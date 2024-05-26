import torch
torch.set_num_threads(1)
import librosa
import numpy
from scipy.signal import find_peaks
from scipy.io import wavfile
import pyworld as pw
import math

def specIndices(sr, speech_timestamps):
    #Converts speech timestamps into spectogram indices
    sp_ind = []
    N = 2048 / 2
    H = 512
    for a in speech_timestamps:
        curr = []
        ss = a["start"] / 16000 * sr
        s = (ss - N) / H
        curr.append(round(s))
        es = a["end"] / 16000 * sr
        e = (es - N) / H
        curr.append(round(e))
        sp_ind.append(curr)
    return sp_ind

def movingAVGnoZero(arr,window_size):
    #Moving average method that ignores zeroes while calculates the average in the given window
    i = 0
    moving_averages = []
    seg_edge = int(window_size/2)
    for j in range(0,seg_edge,1):
        startseg = arr[0:j]
        startseg = [0 if math.isnan(x) else x for x in startseg]
        startseg = [n for n in startseg if n != 0]
        if len(startseg) == 0:
            start_avg = 0
        else:
            start_avg = round(numpy.sum(startseg) / j+1, 2)
        moving_averages.append(start_avg)
    # Loop through the array t o
    # consider every window of size 3
    while i < len(arr) - window_size + 1:
        # Calculate the average of current window
        segment = arr[i:i + window_size]
        segment =[0 if math.isnan(z) else z for z in segment]
        segment = [j for j in segment if j != 0]
        seg_sum = numpy.sum(segment)
        window_average = round(seg_sum / len(segment), 2)
        # Store the average of current
        # window in moving average list
        moving_averages.append(window_average)
        # Shift window to right by one position
        i += 1
    endpart =[]
    for q in range(1,seg_edge,1):
        endseg = arr[-q:-1]
        endseg = [0 if math.isnan(m) else m for m in endseg]
        endseg = [a for a in endseg if a != 0]
        if len(endseg) == 0:
            end_avg = 0
        else:
            end_avg = round(numpy.sum(endseg) / q+1, 2)
        endpart.append(end_avg)
    endpart = list(reversed(endpart))
    moving_averages.extend(endpart)
    return numpy.array(moving_averages)

def smallerSegment(sample, SAMPLING_RATE,start):
    #Turns long segment into smaller segments
    _f0, time = pw.dio(sample, SAMPLING_RATE)
    wsize = 200
    frequency = movingAVGnoZero(_f0, wsize)
    frequency = [0 if math.isnan(m) else m for m in frequency]
    hist, bin_edges = numpy.histogram(frequency, bins=100)
    peaks, _ = find_peaks(hist, height=100, prominence=10)  # Adjust prominence as needed
    newseg = []
    if len(peaks) != 0:
        histseg = hist[peaks[0]:peaks[-1]]
        localmin, _ = find_peaks(-histseg, prominence=10)
        smin_i = 0
        smin = 100
        for i in localmin:
            min_i = peaks[0] + i
            if hist[min_i] <= smin:
                proc = (100 * min_i) / len(bin_edges)
                if 30 <= proc <= 70:
                    smin = hist[min_i]
                    smin_i = min_i
        if smin_i != 0:
            threshold = (bin_edges[smin_i] + bin_edges[smin_i + 1]) / 2
        else:
            threshold = -1
        if threshold != -1:
            speakers = []
            for c in range(len(frequency)):
                if frequency[c] <= threshold:
                    speakers.append(1)
                else:
                    speakers.append(2)
            for sp in range(len(speakers)):
                if sp == 0:
                    s = time[sp]
                    e = time[sp]
                    check = speakers[sp]
                else:
                    if check == speakers[sp]:
                        e = time[sp]
                        if sp == len(speakers) - 1:
                            newseg.append([round(start + s*SAMPLING_RATE,2),  round(start + e*SAMPLING_RATE,2)])
                    else:
                        newseg.append([round(start + s*SAMPLING_RATE,2),  round(start + e*SAMPLING_RATE,2)])
                        s = time[sp]
                        e = time[sp]
                        check = speakers[sp]
            return newseg
        else:
            return newseg
    else:
        return newseg


if __name__ == '__main__':
    SAMPLING_RATE = 16000
    # load Silero-VAD model
    USE_ONNX = False
    model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                  model='silero_vad',
                                  force_reload=True,
                                  onnx=USE_ONNX)

    (get_speech_timestamps,
     save_audio,
     read_audio,
     VADIterator,
     collect_chunks) = utils
    vad_iterator = VADIterator(model)

    # wav file name
    name="test16"
    # wav file path
    audio = "C:/magistras/tiriamasis darbas/garso_irasai/wav_files/" + name + ".wav"
    # Voice activity detection
    wav = read_audio(audio, sampling_rate=SAMPLING_RATE)
    speech_timestamps = get_speech_timestamps(wav, model, sampling_rate=SAMPLING_RATE)

    # Looking for long VAD segments and dividing them into shorter segments
    max_segment_duration = 10.0
    refined_timestamps = []
    sr, samplewav = wavfile.read(audio)
    for i in speech_timestamps:
        start, end = i['start'], i['end']
        segment_duration = (end/SAMPLING_RATE) - (start/SAMPLING_RATE)
        if segment_duration > max_segment_duration:
            sample = samplewav[start:end]
            sample = sample.astype(numpy.double)
            newsegments = smallerSegment(sample, SAMPLING_RATE, start)
            if not newsegments:
                refined_timestamps.append({'start': start, 'end': end})
            else:
                for seg in newsegments:
                    refined_timestamps.append({'start': int(seg[0]), 'end': int(seg[1])})
        else:
            refined_timestamps.append({'start': start, 'end': end})

    # saving labels for Wav2vec
    with open("wav2vec_timestamps/"+name+'_wav2vec_timestamps.txt', 'w') as ffile:
        for i in refined_timestamps:
            currT=[]
            currT.extend([i["start"],i['end']])
            ffile.write(str(currT[0])+","+str(currT[1])+"\n")
    ffile.close()

    # saving labels for spectogram and mel-spectogram
    x, sample_rate = librosa.load(audio)
    sp_ind = specIndices(sample_rate, refined_timestamps)

    with open("spec_timestamps/"+name+'_spec_timestamps.txt', 'w') as sfile:
        for q in sp_ind:
            sfile.write(str(q[0])+","+str(q[1])+"\n")
        sfile.write(str(sample_rate))
    sfile.close()