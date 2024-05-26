from pydub import AudioSegment

def VAread(path):
    file = path.read()
    VAlabels = file.split("\n")
    VAlabels.pop(len(VAlabels) - 1)
    hyp = []
    for j in range(len(VAlabels)):
        VAlabels[j] = VAlabels[j].split(",")
        if VAlabels[j][2] != "NK":
            vasegment = (VAlabels[j][2], float(VAlabels[j][0]), float(VAlabels[j][1]))
            hyp.append(vasegment)
    return hyp

if __name__ == '__main__':
    name = "test8"
    w_path = "C:/magistras/tiriamasis darbas/garso_irasai/wav_files/" + name + ".wav"
    s_path = "C:/magistras/tiriamasis darbas/diar_rez/oracle_segments/"+name+"_oracle_segments.txt"
    wav = AudioSegment.from_wav(w_path)
    silence = AudioSegment.silent()
    seg_file = open(s_path,encoding="UTF-8")
    segments = VAread(seg_file)
    labels = []
    for i in segments:
        if i[0] not in labels:
            labels.append(i[0])
    for l in range(len(labels)):
        check = 0
        for a in range(len(segments)):
            if segments[a][0] == labels[l]:
                if check == 0:
                    new_wav = silence+wav[segments[a][1]*1000:segments[a][2]*1000]+silence
                    check += 1
                else:
                    new_wav = new_wav + wav[segments[a][1]*1000:segments[a][2]*1000]+silence
        nr =l+1
        new_wav.export("kalba_"+str(nr)+".wav", format="wav")