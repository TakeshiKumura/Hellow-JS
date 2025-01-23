import sys
import pyttsx3
import time
import threading
import re
from PyPDF2 import PdfReader
from PIL import Image

def extract_text_from_pdf(pdf_path):
    """PDFファイルからテキストを抽出する関数"""
    text = ""
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()

def extract_text_from_txt(txt_path):
    """TXTファイルからテキストを抽出する関数"""
    with open(txt_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

# 音声合成関数
def speech_text(text, lang, times):
    """指定された言語でテキストを音声合成する関数"""
    start_time = time.time()  # 音声再生開始時刻
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    voice_id = voices[0].id  # デフォルト音声を使用

    engine.setProperty("voice", voice_id)
    engine.say(text)
    engine.runAndWait()
    end_time = time.time()  # 音声再生終了時刻
    times['speak'] = end_time - start_time  # 経過時間記録

# 文字を逐次表示する関数
def print_text(text, speech_duration):
    """テキストを1文字ずつ表示する関数"""
    start_time = time.time()  # テキスト表示開始時刻
    display_duration = speech_duration / len(text)  # 1文字あたりの表示時間
    for char in text:
        print(char, end='', flush=True)
        time.sleep(display_duration)  # 音声進行に合わせて表示を遅延
    end_time = time.time()  # テキスト表示終了時刻
    return end_time - start_time  # テキスト表示時間を返す

# テキストを処理し、言語に応じて音声合成する関数
def process_text(text):
    """テキストを処理し、音声合成と表示を行う"""
    parts = re.split(r'([、。,.])', text)  # テキストを句読点で分割
    output_info = []  # 出力情報を保持するリスト
    times = {}  # 処理時間を記録する辞書

    for part in parts:
        part = part.strip()
        if not part or part in ['.', '。', ',', '、']:
            continue  # 空部分や句読点はスキップ

        # 音声再生スレッド
        speech_thread = threading.Thread(target=speech_text, args=(part, 'ja', times))
        speech_thread.start()

        # テキスト表示スレッド（音声再生時間を利用）
        display_duration = print_text(part, times.get('speak', 1))
        speech_thread.join()  # 音声再生が完了するまで待つ

        # テキスト表示時間を取得し、出力情報に追加
        total_time = times.get('speak', 0) + display_duration
        output_info.append(f"音声再生時間: {times.get('speak', 0):.2f}秒 | テキスト表示時間: {display_duration:.2f}秒")

    # 一度に出力
  
