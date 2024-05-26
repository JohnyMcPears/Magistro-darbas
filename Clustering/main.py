import numpy as np
from sklearn.cluster import KMeans

def spec_labels(ts, spec, wavS,cluster):
    #  Generates speech labels using spectogram or mel-spectogram features
    vs = []
    for j in ts:
        curr = []
        for q in range(j[0] - 1, j[1]):
            curr.append(spec[q])
        cmean = np.mean(curr, axis=0)
        vs.append(cmean)
    labels = KMeans(n_clusters=cluster, n_init="auto").fit(vs).labels_
    for e in range(len(ts)):
        ts[e].append(labels[e])
    min = 0
    timestamps = []
    for a in range(len(ts)):
        if ts[a][0] > min:
            timestamps.append([min, ts[a][0], "NK"])
            timestamps.append(ts[a])
            min = ts[a][1]
        else:
            timestamps.append(ts[a])
            min = ts[a][1]
        if a == len(ts) - 1:
            if ts[a][1] != wavS:
                timestamps.append([ts[a][1], wavS, "NK"])
    return timestamps

def fair_labels(ts2, fair, wavFS,cluster):
    # Generates speech labels using wav2vec features
    vf = []
    for i in ts2:
        curr = []
        for q in range(i[0] - 1, i[1]):
            curr.append(fair[q])
        cmean = np.mean(curr, axis=0)
        vf.append(cmean)
    labels = KMeans(n_clusters=cluster, n_init="auto").fit(vf).labels_
    for s in range(len(ts2)):
        ts2[s].append(labels[s])
    print(ts2)
    min = 0
    timestamps = []
    for a in range(len(ts2)):
        if ts2[a][0] > min:
            timestamps.append([min, ts2[a][0], "NK"])
            timestamps.append(ts2[a])
            min = ts2[a][1]
        else:
            timestamps.append(ts2[a])
            min = ts2[a][1]
        if a == len(ts2) - 1:
            if ts2[a][1] != wavFS:
                timestamps.append([ts2[a][1], wavFS, "NK"])
    return timestamps
if __name__ == '__main__':
    cluster = 2
    N=2048/2
    H=512
    # wav file name
    name = "test19"
    # Generating speech labels with spectogram or mel-spectogram

    # path for spectogram timestamps
    textfile = open("D:/Pydarbai/spec2labels/spec_timestamps/"+name+"_spec_timestamps.txt", encoding="UTF-8")
    file = textfile.read()
    ts = file.split("\n")
    sr = int(ts[len(ts) - 1])
    ts.pop(len(ts) - 1)
    for i in range(len(ts)):
        ts[i] = ts[i].split(",")
        ts[i][0]=int(ts[i][0])
        ts[i][1] = int(ts[i][1])

    #load spectogram or mel-spectogram
    #spec = np.load("D:/Pydarbai/spectogram/spec/"+name+"_spectogram.npy").T
    spec = np.load("D:/Pydarbai/spectogram/mel-spec/"+name+"_spectogram.npy").T
    wavS=len(spec)
    spec_stamps=spec_labels(ts, spec, wavS,cluster)
    # Saving generated speech labels using spectogram or  mel-spectogram
    #with open("spec_segments/"+name+"_spec_segments.txt", 'w',encoding='utf-8') as f:
    with open("mel-spec_segments/"+name+"_mel-spec_segments.txt", 'w',encoding='utf-8') as f:
        for m in spec_stamps:
            if m[0] != 0:
                timemin = (m[0] * H + N) / sr
            else:
                timemin = 0
            timemax = (m[1] * H + N) / sr
            f.write(str(timemin)+","+str(timemax)+","+str(m[2])+"\n")
    f.close()

    # Generating speech labels with wav2vec extracted features
    # path for wav2vec timestamps
    textfile2 = open("D:/Pydarbai/spec2labels/wav2vec_timestamps/"+name+"_fair_timestamps.txt", encoding="UTF-8")
    file2 = textfile2.read()
    ts2 = file2.split("\n")
    ts2.pop(len(ts2) - 1)
    for j in range(len(ts2)):
        ts2[j] = ts2[j].split(",")
        ts2[j][0]=int(ts2[j][0])
        ts2[j][1] = int(ts2[j][1])
    #load wav2vec extracted features
    fair = np.load("D:/Pydarbai/spectogram/wav2vec/"+name+"_fairseq.npy").T
    wavFS=len(fair)

    fair_stamps=fair_labels(ts2, fair, wavFS,cluster)
    # Saving generated speech labels using wav2vec
    with open("wav2vec_segments/"+name+"_wav2vec_segments.txt", 'w',encoding='utf-8') as ff:
        for n in fair_stamps:
            if n[0] != 0:
                timemin = n[0] / 16000
            else:
                timemin = 0
            timemax = n[1] / 16000
            ff.write(str(timemin)+","+str(timemax)+","+str(n[2])+"\n")
    ff.close()