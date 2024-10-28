import os


# 读取文件并排序
def sort_words_from_file(input_file, output_file):
    with open(input_file, 'r') as file:
        content = file.read()

    sorted_words = sorted(content.split())  # 使用split分割内容，sorted进行排序
    output_content = ' '.join(sorted_words)  # 使用join合并排序后的单词

    with open(output_file, 'w') as file:
        file.write(output_content)


# 主程序
if __name__ == "__main__":
    input_file = 'input.txt'  # 输入文件名
    output_file = 'output.txt'  # 输出文件名
    sort_words_from_file(input_file, output_file)