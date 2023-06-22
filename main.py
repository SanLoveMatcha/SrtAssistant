import os
import sys

import four_txt_plus_srt
import one_srt_emerge
import three_gpt_en_to_zh
import two_srt_to_txt


def main():
    # 输入文件名
    input_file = input("请输入当前目录下需要翻译的文件：")

    # 调用one_srt_emerge.py中的main函数
    merged_file = one_srt_emerge.main(input_file)

    # 调用two_srt_to_txt.py中的函数
    convert_srt_file = two_srt_to_txt.convert_srt_to_txt(merged_file)

    # 调用 three_gpt_en_to_zh.py中的函数
    translation_file = three_gpt_en_to_zh.main(convert_srt_file)
    print(f"翻译完成！已保存到文件: {translation_file}")

    # 输入最终输出文件名
    output_file = input("请输入生成的最终文件名（请包括你想要的.xxx后缀名）：")

    # 调用four_txt_plus_srt.py中的函数
    done_file = four_txt_plus_srt.main(merged_file, translation_file, output_file)

    print("本次翻译已完成！")


if __name__ == "__main__":
    main()
