# synthesize_audio.py
# synthesize_audio.py
from model import create_model

def generate_audio_from_text(model, text):
    mel_output = model.predict([text])  # テキストからメルスペクトログラム生成
    waveform = generate_waveform_from_mel(mel_output)  # メルスペクトログラムから波形を生成
    return waveform
