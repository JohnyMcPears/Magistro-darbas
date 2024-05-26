from pyannote.metrics.diarization import DiarizationErrorRate
from pyannote.core import Annotation, Segment
import matplotlib
matplotlib.use('Agg')
import re

def tgread(path):
    # read textgrid file
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

def VAread(path):
    file = path.read()
    VAlabels = file.split("\n")
    VAlabels.pop(len(VAlabels) - 1)
    hyp = []
    for j in range(len(VAlabels)):
        VAlabels[j] = VAlabels[j].split(",")
        label = ""
        if VAlabels[j][2] != "NK":
            if VAlabels[j][2] == "NT":
                label = VAlabels[j][2]
            else:
                label = "kalba_" + VAlabels[j][2]
            vasegment = (label, float(VAlabels[j][0]), float(VAlabels[j][1]))
            hyp.append(vasegment)
    return hyp

def textgrid2seg(seg):
    list=[]
    for i in range(5,len(seg),3):
        if seg[i+2] != '""' and seg[i+2] != '"NK"' and seg[i+2] != '"Nk"':
            l=seg[i+2].replace('"', '')
            segment=(l,float(seg[i]),float(seg[i+1]))
            list.append(segment)
    return list

def rttm2seg(seg,ml):
    list=[]
    for i in range(3,len(seg),10):
        if float(seg[i]) < ml:
            segment=(seg[i+4],float(seg[i]),float(seg[i+1])+float(seg[i]))
        else:
            segment = (seg[i + 4], float(seg[i]), float(ml))
        list.append(segment)
    return list

if __name__ == '__main__':
    #folder name
    filen= "spec_segments"

    #wav file name
    name = "test19"
    #load correct reference segments
    TG = open("C:/magistras/tiriamasis darbas/diar_rez/textgrid/" + name + "_p_s.textgrid", encoding="UTF-8")
    tgseg = tgread(TG)
    maxl = tgseg[3]
    realseg = textgrid2seg(tgseg)

    # choose which segments you load as hypothesis segments
    #load RTTM segment file from other diarization tools
    """RTTM = open("C:/magistras/tiriamasis darbas/diar_rez/" + filen + "_rttm/" + name + "_hyp.rttm", encoding="UTF-8")
    file2 = RTTM.read()
    rttmseg = re.split(" |\n", file2)
    rttmseg.pop(len(rttmseg) - 1)
    newhyp = rttm2seg(rttmseg, float(maxl))"""

    #load segments that the segmentation algorithm created
    VAfile = open("C:/magistras/tiriamasis darbas/diar_rez/" + filen + "/" + name + "_" + filen + ".txt",encoding="UTF-8")
    newhyp = VAread(VAfile)

    #Creating annotations for DER tool
    reference = Annotation()
    hypothesis = Annotation()
    for i in realseg:
        reference[Segment(float(i[1]), float(i[2]))] = i[0]
    for j in newhyp:
        hypothesis[Segment(float(j[1]), float(j[2]))] = j[0]

    # calculate DER
    DER = DiarizationErrorRate()
    res = DER(reference, hypothesis, detailed=True, uem=Segment(0, float(maxl)))
    report = DER.report(display=True)

    #Save DER in file
    with open(filen + '_der_results.txt', 'a', encoding='utf-8') as f:
        f.write(name + "\n")
        for q in res:
            f.write(str(q) + ": " + str(res[q]))
            f.write("\n")
        f.write("\n")
        f.write("-" * 65)
        f.write("\n")