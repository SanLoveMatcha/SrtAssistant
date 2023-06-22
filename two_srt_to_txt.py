import os


def convert_srt_to_txt(filename):
    # 调用第一个python文件中的main函数，并获取返回的文件名
    print(f"2.即将处理该文件: {filename}")

    with open(filename, 'r', encoding='utf-8') as file:
        srt_text = file.read()

    blocks = srt_text.strip().split('\n\n')  # Stipe()去除输入字符串的首尾空格，split()连续的两个换行符\n\n进行拆分，得到每个字幕块。
    txt_lines = []

    for block in blocks:
        lines = block.split('\n')
        if len(lines) >= 3:  # srt字幕 一行序号 一行时间轴 第三行为内容
            text = ' '.join(lines[2:])
            txt_lines.append(text)

    txt_text = '\n'.join(txt_lines)

    # 生成输出文件的名称
    output_filename = os.path.splitext(filename)[0] + '_2.txt'

    # 将转换后的内容保存到文件中
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write(txt_text)

    print(f"转换完成！已将srt字幕转换为txt格式并保存到文件'{output_filename}'中。")

    return output_filename
