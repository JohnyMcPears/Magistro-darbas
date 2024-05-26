def tgread(path):
    #Reads textgrid file
    file = path.read()
    seg = file.split("IntervalTier")
    seg.pop(0)
    if len(seg) == 1:
        seg = seg[0].split("\n")
        seg.pop(len(seg) - 1)
    else:
        for i in range(len(seg)):
            seg[i] = seg[i].split("\n")
            seg[i].pop(len(seg[i]) - 1)
        seg = seg[0] + seg[1][5:len(seg[1])]
    return seg

def textgrid2seg(seg):
    #turns textgrid into simple list with segments
    list=[]
    for i in range(5,len(seg),3):
        if seg[i+2] != '""' and seg[i+2] != '"NK"' and seg[i+2] != '"Nk"':
            l=seg[i+2].replace('"', '')
            segment=(l,float(seg[i]),float(seg[i+1]))
            list.append(segment)
    return list

def OracleRead(path):
    #Reads oracle segment file
    file = path.read()
    timestamps = file.split("\n")
    timestamps.pop(0)
    timestamps = [i.split(",") for i in timestamps]
    timestamps.pop(-1)
    for i in range(len(timestamps)):
        timestamps[i] = [float(x) for x in timestamps[i]]
    return timestamps

def getOverlap(a, b):
    return max(0, min(a[1], b[1]) - max(a[0], b[0]))

if __name__ == '__main__':
    # wav file name
    name = "test1"
    # textgrid file path
    TG = open("C:/magistras/tiriamasis darbas/diar_rez/textgrid/" + name + "_p_s.textgrid", encoding="UTF-8")
    tgseg = tgread(TG)
    maxl = tgseg[3]
    realseg = textgrid2seg(tgseg)
    # oracle file path
    O = open("C:/magistras/tiriamasis darbas/VAD/oracle_labels/" + name + "_oracle_timestamps.txt", encoding="UTF-8")
    timestamps = OracleRead(O)
    oracle_l = []
    oracle_t = []
    #gets new oracle time and lables into two lists
    for a in timestamps:
        clabel = []
        ctime=[]
        for seg in realseg:
            interval2 = [seg[1],seg[2]]
            result = getOverlap(a,interval2)
            if result > 0:
                if seg[0] not in clabel:
                    clabel.append(seg[0])
                    ctime.append(result)
                else:
                    si = clabel.index(seg[0])
                    ctime[si] = ctime[si]+result
        if len(clabel) == 0 and len(ctime) == 0:
            clabel.append("NK")
            ctime.append(0)
        oracle_l.append(clabel)
        oracle_t.append(ctime)
    #Categorizes oracle segments using the new oracle time and labels lists
    for i in range(len(oracle_l)):
        if len(oracle_l[i]) == 1:
            timestamps[i].append(oracle_l[i][0])
        else:
            mx = max(oracle_t[i])
            mxi = oracle_t[i].index(mx)
            if "NT" == oracle_l[i][mxi]:
                sm = sorted(oracle_t[i])[-2]
                smi = oracle_t[i].index(sm)
                timestamps[i].append(oracle_l[i][smi])
            else:
                timestamps[i].append(oracle_l[i][mxi])
    #Makes the NT segments into one big NT segment
    ifnt = any("NT" in sublist for sublist in timestamps)
    if ifnt == True:
        ms = 0
        for e in range(len(timestamps)-1,0,-1):
            if timestamps[e][2] == "NT":
                ms = timestamps[e][0]
                timestamps.pop(e)
            else:
                timestamps.append([ms, maxl, "NT"])
                break
    #Writes the new oracle file with categorized segments
    with open("oracle_segments/" + name + "_oracle_segments.txt", 'w', encoding='utf-8') as of:
        for n in timestamps:
            of.write(str(n[0]) + "," + str(n[1]) + "," + str(n[2]) + "\n")
    of.close()