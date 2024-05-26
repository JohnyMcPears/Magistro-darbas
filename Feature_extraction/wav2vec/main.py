import numpy as np
import soundfile as sf
from transformers import Wav2Vec2Processor

if __name__ == '__main__':
    # wav file name
    name = "test1"
    # wav file path
    path="D:/Pydarbai/tool_pasibandymai/wav_files/"+name+".wav"
    audio_input, sample_rate = sf.read(path)

    #load wav2vec model
    processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")

    # pad input values and return pt tensor
    input_values = processor(audio_input, sampling_rate=sample_rate, return_tensors="np").input_values

    # save wav2vec tensor as npy file
    with open(name+'_wav2vec.npy', 'wb') as f:
        np.save(f, input_values)
