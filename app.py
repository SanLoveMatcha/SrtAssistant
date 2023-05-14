from flask import Flask, request, send_file
import openai
import pysrt
import tempfile
import os

app = Flask(__name__)

# 你的OpenAI API密钥
openai.api_key = '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'

@app.route('/translate', methods=['POST'])
def translate():
    file = request.files['file']
    if file:
        # 读取并解析srt文件
        subs = pysrt.open(file=file.stream)

        # 将每一行字幕通过OpenAI的ChatGPT API进行翻译
        for sub in subs:
            response = openai.Completion.create(engine="text-davinci-003", prompt=sub.text, max_tokens=60)
            sub.text = response.choices[0].text.strip()

        # 将翻译后的字幕保存到临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.srt') as fp:
            subs.save(fp.name, encoding='utf-8')
            temp_filename = fp.name

        # 将临时文件发送到客户端
        return send_file(temp_filename, as_attachment=True, attachment_filename='translated.srt')

    return 'No file uploaded', 400

if __name__ == "__main__":
    app.run(port=5000)
