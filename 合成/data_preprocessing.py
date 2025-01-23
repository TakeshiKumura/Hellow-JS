# data_preprocessing.py

import librosa
import librosa.display
import numpy as np

def preprocess_audio(file_path):
    # 音声ファイルの読み込み
    y, sr = librosa.load("your_audio_file.wav", sr=None)

    # メルスペクトログラムの抽出
    mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=80)
    return mel_spectrogram
# メルスペクトログラムの表示
import matplotlib.pyplot as plt
librosa.display.specshow(librosa.power_to_db(mel_spectrogram, ref=np.max), y_axis='mel', x_axis='time')
plt.colorbar(format='%+2.0f dB')
plt.show()
