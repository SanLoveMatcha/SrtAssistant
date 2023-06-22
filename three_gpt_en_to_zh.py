import os
import openai
os.environ["http_proxy"]="127.0.0.1:7890"
os.environ["https_proxy"]="127.0.0.1:7890"

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key= os.environ['OPENAI_API_KEY']
def split_text(file_path, max_tokens=2048):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    text = text.replace('。', '。\n')  # 每个句号后面加个回车
    # Break the text up into chunks approximately max_tokens in length
    text_segments = []
    current_segment = ''
    for line in text.split('\n'):
        if len((current_segment + line).split()) <= max_tokens:
            current_segment += line + '\n'
        else:
            text_segments.append(current_segment)
            current_segment = line + '\n'
    text_segments.append(current_segment)
    # Add a print statement to check the segments
    for i, segment in enumerate(text_segments):
        print(f"这是传送给api的内容块 {i + 1}: {segment}")
    return text_segments


def translate_text(text_segments, api_key, prompt, model='gpt-3.5-turbo'):
    openai.api_key = api_key
    translated_segments = []
    for segment in text_segments:
        response = openai.ChatCompletion.create(
            model=model, temperature=0.5,
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a helpful English to Simplified Chinese translation assistant.You will translate the following context and strictly making sure to each sentence seperated by a period must be translated independently,even if this might result in semantic inconsistencies.The translated text has as many sentences as there should be as many sentences as the translated text should be.Any terminology not recognized in your database should remain untranslated to prevent any errors.Please do not put quotation marks when output.Each translated sentence ends with a Chinese period.Input Example:And for me to be at my most alert and focused throughout the day and to optimize my sleep at night.So what I do is I get out of bed and I go outside.Output Example:为了让自己整天都能保持警觉和专注，并在夜间优化睡眠。所以我的做法是起床然后出门。'
                },
                {
                    'role': 'user',
                    'content': prompt + segment
                }
            ]

        )
        translated_segment = response['choices'][0]['message']['content'].strip()
        translated_segments.append(translated_segment)

        token_dict = {
            'prompt_tokens': response['usage']['prompt_tokens'],
            'completion_tokens': response['usage']['completion_tokens'],
            'total_tokens': response['usage']['total_tokens'],
        }
        print(token_dict)
        print("")
    return translated_segments
    # time.sleep(180)  # 3 minutes sleep to avoid overuse


def save_translated_text(translated_segments, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for i, segment in enumerate(translated_segments):
            # Add a newline after each period
            segment = segment.replace('。', '。\r')
            print(f"这是从api得到的内容块 {i + 1} : {segment}")
            print("")
            if i < len(translated_segments) - 1:  # 不是最后一个段落
                file.write(segment + '\n')  # 加上换行符
            else:  # 是最后一个段落
                file.write(segment)  # 不添加换行符

def main(convert_srt_file):
    print(f"3.即将调用api翻译该文件: {convert_srt_file}\n")
    file_path = f"{convert_srt_file}"  # 获取第二个函数生成的文件名
    prompt = f""" """
    text_segments = split_text(file_path)
    translated_segments = translate_text(text_segments, openai.api_key, prompt)
    output_file_path = os.path.splitext(convert_srt_file)[0] + '_3.txt'
    save_translated_text(translated_segments, output_file_path)
    print("3.已接受所有从api获取的翻译内容")
    return output_file_path


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        convert_srt_file = sys.argv[1]
    else:
        print("请在命令行中指定 convert_srt_to_txt.py 生成的文件名作为参数。")
        sys.exit(1)
    main(convert_srt_file)
