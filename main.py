"""
This is the main module for the paper check program.
It compares two text files and calculates their similarity.
"""

import sys
import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def read_file(file_path):
    """
    读取文件内容。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # 如果 UTF-8 解码失败，尝试使用 GBK 编码
        with open(file_path, 'r', encoding='gbk') as f:
            return f.read()


def preprocess_text(text):
    """
    文本预处理：分词并去除停用词。
    """
    words = jieba.lcut(text)
    stop_words = set(['的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好'])
    filtered_words = [word for word in words if word not in stop_words]
    return ' '.join(filtered_words)


def calculate_similarity(text1, text2):
    """
    计算两段文本的余弦相似度。
    """
    vectorizer = CountVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    similarity = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
    return round(similarity, 2)


def main(args=None):
    """
    主函数：比较两个文件的相似度。
    """
    if args is None:
        args = sys.argv[1:]

    if len(args) != 3:
        print("Usage: python main.py <original_file> <copied_file> <output_file>")
        sys.exit(1)

    original_file = args[0]
    copied_file = args[1]
    output_file = args[2]

    try:
        original_text = read_file(original_file)
        copied_text = read_file(copied_file)
    except FileNotFoundError as e:
        print(f"文件未找到: {e.filename}")
        sys.exit(1)

    original_processed = preprocess_text(original_text)
    copied_processed = preprocess_text(copied_text)

    similarity = calculate_similarity(original_processed, copied_processed)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"{similarity:.2f}")


if __name__ == "__main__":
    main()