import sys


def replace_subtitle(srt_file, translation_file, output_file):
    with open(srt_file, 'r', encoding='utf-8') as f:
        srt_data = f.readlines()

    with open(translation_file, 'r', encoding='utf-8') as f:
        translation_data = [line.strip() for line in f.readlines() if line.strip() != '']

    assert len(srt_data) == len(
        translation_data), f"警告: 原始字幕文件和翻译文件的字幕数量不匹配. 原始文件有 {len(srt_data)} 块字幕, 翻译文件有 {len(translation_data)} 行翻译文本."

    new_srt_data = ''
    translation_index = 0
    for line in srt_data:
        if line.strip().isdigit() or '-->' in line:
            new_srt_data += line
        elif line.strip() != '':
            new_srt_data += translation_data[translation_index] + '\n'
            translation_index += 1
        else:
            new_srt_data += '\n'

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_srt_data)
        print(f"时间轴已合并，最终字幕已生成并保存为{output_file}文件。")


def main(srt_file, translation_file, output_file):
    replace_subtitle(srt_file, translation_file, output_file)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("您未提供足够的参数：合并过后的 srt 文件、已翻译好的 txt 文件的路径、生成文件名。")
        srt_file = input("请输入合并过后的srt文件：")
        translation_file = input("请输入已翻译好的txt文件的路径：")
        output_file = input("请输入生成文件名：")
    else:
        srt_file = sys.argv[1]
        translation_file = sys.argv[2]
        output_file = sys.argv[3]

    main(srt_file, translation_file, output_file)
