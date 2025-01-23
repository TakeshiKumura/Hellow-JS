import sys
import pyttsx3
import time
import threading
import re
from PyPDF2 import PdfReader

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
    
    # 空白と改行をスキップしてテキストを読み上げる
    text_to_speak = re.sub(r'\s+', ' ', text).strip()  # 空白と改行を単一の空白に置き換える
    engine.say(text_to_speak)
    engine.runAndWait()
    end_time = time.time()  # 音声再生終了時刻
    times['speak'] = end_time - start_time  # 経過時間記録
    
    if "。" in text:  # 読み上げた内容に「。」が含まれている場合、終了
        print("「。」を読み上げたので終了します。")
        sys.exit(0)

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

def search_and_process_text(text, search_term):
    """検索語に一致する部分を抽出し、音声合成と表示を行う関数"""
    # 検索語に一致する部分を抽出
    matches = re.finditer(search_term, text)
    output_info = []  # 出力情報を保持するリスト
    times = {}  # 処理時間を記録する辞書

    for match in matches:
        part = match.group(0)  # 検索語に一致した部分
        
        # 音声再生スレッド
        speech_thread = threading.Thread(target=speech_text, args=(part, 'ja', times))
        speech_thread.start()

        # テキスト表示スレッド（音声再生時間を利用）
        display_duration = print_text(part, times.get('speak', 1))
        speech_thread.join()  # 音声再生が完了するまで待つ

        # テキスト表示時間を取得し、出力情報に追加
        total_time = times.get('speak', 0) + display_duration
        output_info.append(f"音声再生時間: {times.get('speak', 0):.2f}秒 | テキスト表示時間: {display_duration:.2f}秒")

        # 読み上げが終わった時点で検索を終了
        print(" | ".join(output_info))
        break  # 検索語が見つかったら終了

def process_file(file_path, search_term):
    """ファイルの種類に応じてテキストを抽出し処理する関数"""
    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.txt'):
        text = extract_text_from_txt(file_path)
    else:
        print("サポートされていないファイル形式です。")
        return

    search_and_process_text(text, search_term)

def interactive_mode():
    """対話モードを実行する関数"""
    print("対話モードに入ります。テキストを入力してください。終了するには「終了」と入力してください。")
    while True:
        user_input = input("> ")
        if user_input.strip().lower() == "終了":
            print("プログラムを終了します。")
            break
        search_term = input("検索語を入力してください: ")
        search_and_process_text(user_input, search_term)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        input_file = sys.argv[1]
        search_term = sys.argv[2]
        if input_file.endswith(('.pdf', '.txt')):
            try:
                process_file(input_file, search_term)
            except Exception as e:
                print(f"ファイル処理中にエラーが発生しました: {e}")
                # 対話モードを実行
                interactive_mode()
        else:
            print("PDFまたはTXTファイルを引数として渡してください。")
            sys.exit(1)
