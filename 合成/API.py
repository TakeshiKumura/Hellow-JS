from transformers import pipeline

# GPT-2 モデルを使用するための pipeline の設定
generator = pipeline("text-generation", model="gpt2", framework="pt")

# テキスト生成
text = generator("Once upon a time", max_length=50, num_return_sequences=1)

# 生成したテキストを出力
print(text[0]['generated_text'])
