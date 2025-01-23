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

# 言語と音声インデックスの対応表
voice_dict = {
    'ja': 0,  # Microsoft Haruka - Japanese
    'en': 1,  # Microsoft Zira - English (United States)
    'es': 2,  # Microsoft Helena - Spanish (Spain)
    'fr': 3,  # Microsoft Hortense - French
    'it': 4,  # Microsoft Elsa - Italian (Italy)
    'de': 5,  # Microsoft Hedda - German
    'pl': 6   # Microsoft Paulina - Polish
}

def speech_text(text, lang, times):
    """指定された言語でテキストを音声合成する関数"""
    start_time = time.time()  # 音声再生開始時刻
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    
    # 言語に応じた音声を選択
    if lang in voice_dict:
        voice_id = voices[voice_dict[lang]].id
    else:
        voice_id = voices[0].id  # デフォルト音声

    engine.setProperty("voice", voice_id)
    engine.say(text)
    engine.runAndWait()
    end_time = time.time()  # 音声再生終了時刻
    times['speak'] = end_time - start_time  # 経過時間記録

def print_text(text, speech_duration):
    """テキストを一文字ずつ表示する関数"""
    start_time = time.time()  # テキスト表示開始時刻
    for char in text:
        print(char, end='', flush=True)
        time.sleep(speech_duration / len(text))
    end_time = time.time()  # テキスト表示終了時刻
    return end_time - start_time  # テキスト表示時間を返す

def detect_language(text):
    """文字列に基づいて日本語か英語を判別する関数"""
    japanese_characters = re.findall(r'[ぁ-んァ-ン一-龥]', text)
    english_characters = re.findall(r'[A-Za-z]', text)
    
    if len(japanese_characters) > len(english_characters):
        return 'ja'  # 日本語
    else:
        return 'en'  # 英語

def process_text(text):
    """テキストを処理し、言語に応じて音声合成する関数"""
    parts = re.split(r'([、。,.]\s+\n)', text)  # テキストを句読点で分割
    default_lang = detect_language(text)  # テキスト全体の言語を事前に判別
    output_info = []  # 出力情報を保持するリスト

    # 直前のテキスト部分を保持するための変数
    previous_part = ""

    for i, part in enumerate(parts):
        part = part.strip()
        if not part or part in ['.', '。', ',', '、']:
            continue  # 空部分や句読点はスキップ

        # 言語設定
        lang = default_lang
        lang_name = '日本語' if lang == 'ja' else '英語'
        times = {}  # 処理時間を記録する辞書

        # 音声再生スレッド
        speech_thread = threading.Thread(target=speech_text, args=(part, lang, times))
        speech_thread.start()

        # テキスト表示スレッド（音声再生時間を利用）
        display_duration = print_text(part, times.get('speak', 1))
        speech_thread.join()  # 音声再生が完了するまで待つ

        # テキスト表示時間を取得し、出力情報に追加
        total_time = times.get('speak', 0) + display_duration
        output_info.append(f"言語: {lang_name} 音声再生時間: {times.get('speak', 0):.2f}秒 | テキスト表示時間: {display_duration:.2f}秒")

        # 直前の部分を更新
        previous_part = part

    # 一度に出力
    print(" | ".join(output_info))

def process_file(file_path):
    """ファイルの種類に応じてテキストを抽出し処理する関数"""
    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.txt'):
        text = extract_text_from_txt(file_path)
    else:
        print("サポートされていないファイル形式です。")
        return

    process_text(text)

def interactive_mode():
    """対話モードを実行する関数"""
    print("対話モードに入ります。テキストを入力してください。終了するには「終了」と入力してください。")
    while True:
        user_input = input("> ")
        if user_input.strip().lower() == "終了":
            print("プログラムを終了します。")
            break
        process_text(user_input)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        input_text = sys.argv[1]
        if input_text.endswith(('.pdf', '.txt')):
            # ファイルとして処理
            try:
                process_file(input_text)
            except Exception as e:
                print(f"ファイル処理中にエラーが発生しました: {e}")
                # 対話モードを実行
                interactive_mode()
        else:
            print("PDFまたはTXTファイルを引数として渡してください。")
            sys.exit(1)
