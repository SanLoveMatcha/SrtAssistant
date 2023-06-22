import os
import sys


def merge_subtitles(file_name):

    with open(file_name, 'r') as file:
        input_srt = file.read()

    # Split input into lines
    lines = input_srt.strip().split('\n')

    # Parse input lines into structured subtitles
    subtitles = []
    i = 0
    while i < len(lines):
        index = int(lines[i])
        times = lines[i + 1]
        text = []
        j = i + 2
        while j < len(lines) and lines[j].strip() != '':
            text.append(lines[j])
            j += 1
        subtitles.append({'index': index, 'times': times, 'text': ' '.join(text)})
        i = j + 1

    # Merge subtitles according to rules
    merged_subtitles = []
    i = 0
    while i < len(subtitles):
        current_subtitle = subtitles[i]
        while i + 1 < len(subtitles) and (
                current_subtitle['text'].strip().endswith(',') or current_subtitle['text'].split()[-1].isalpha()):
            next_subtitle = subtitles[i + 1]
            current_subtitle['text'] = current_subtitle['text'] + ' ' + next_subtitle['text']
            current_subtitle['times'] = current_subtitle['times'].split(' --> ')[0] + ' --> ' + \
                                        next_subtitle['times'].split(' --> ')[1]
            if next_subtitle['text'].strip().endswith('.'):
                i += 1
                break
            i += 1
        merged_subtitles.append(current_subtitle)
        i += 1

    # Format merged subtitles for output
    output = ""
    for idx, subtitle in enumerate(merged_subtitles):
        output += str(idx + 1) + '\n' + subtitle['times'] + '\n' + subtitle['text'] + '\n\n'
    return output.strip()


def main(input_file_name):  # 添加参数 input_file_name
    # 从文件名中提取文件名部分（去除扩展名部分）
    file_name_without_extension = os.path.splitext(input_file_name)[0]

    # 添加"_emerged"到文件名部分，生成新的文件名
    output_file_name = file_name_without_extension + "_merged_1.txt"

    # 将新的文件名和当前工作目录合并，生成完整的文件路径
    output_file_path = os.path.join(os.getcwd(), output_file_name)

    # 合并字幕
    output_srt = merge_subtitles(input_file_name)

    # 将合并后的字幕保存到文件中
    with open(output_file_name, 'w') as file:
        file.write(output_srt)

    print("1.合并后的文件保存为", output_file_path)

    return output_file_name


if __name__ == "__main__":
    main(sys.argv[1])
