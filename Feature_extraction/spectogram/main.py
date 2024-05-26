import numpy as np
import librosa.display

if __name__ == '__main__':
    #wav file name
    name = "test19"
    #wav file path
    path="D:/Pydarbai/tool_pasibandymai/wav_files/"+name+".wav"
    x, sr = librosa.load(path)

    #extract short-long fourier transform
    frameSize = 2048
    hopSize = 512
    S_scale = librosa.stft(x, n_fft=frameSize, hop_length=hopSize)
    #Calculate spectogram
    X_scale= np.abs(S_scale) ** 2
    #Calculate mel-spectogram
    S=librosa.feature.melspectrogram(S=X_scale, sr=sr)
    Log_spec=librosa.power_to_db(S)

    #save spectogram as npy file
    with open(name+'_spectogram.npy', 'wb') as f:
        np.save(f, Log_spec)