import pytest
import main
import os


def test_read_file(tmpdir):
    """
    测试 read_file 函数。
    构造测试数据：创建一个临时文件并写入内容。
    """
    file_path = tmpdir.join("test_file.txt")
    file_path.write("这是一个测试文件。")
    content = main.read_file(file_path)
    assert content == "这是一个测试文件。"


def test_preprocess_text():
    """
    测试 preprocess_text 函数。
    构造测试数据：提供一个包含停用词的句子。
    """
    text = "这是一个测试句子"
    processed_text = main.preprocess_text(text)
    assert processed_text == "这是 一个 测试 句子"


def test_calculate_similarity():
    """
    测试 calculate_similarity 函数。
    构造测试数据：提供两段相似的文本。
    """
    text1 = "这是一个测试句子"
    text2 = "这是另一个测试句子"
    similarity = main.calculate_similarity(text1, text2)
    assert 0 <= similarity <= 1


def test_main_missing_args(capsys):
    """
    测试 main 函数在缺少命令行参数时的情况。
    构造测试数据：不提供任何参数。
    """
    with pytest.raises(SystemExit):
        main.main([])
    captured = capsys.readouterr()
    assert "Usage: python main.py <original_file> <copied_file> <output_file>" in captured.out


def test_main_file_not_found(tmpdir):
    """
    测试 main 函数在文件不存在时的情况。
    构造测试数据：提供不存在的文件路径。
    """
    original_file = tmpdir.join("original.txt")
    copied_file = tmpdir.join("copied.txt")
    output_file = tmpdir.join("output.txt")
    with pytest.raises(SystemExit):
        main.main([original_file, copied_file, output_file])


def test_main_empty_files(tmpdir):
    """
    测试 main 函数在处理空文件时的情况。
    构造测试数据：创建两个空文件。
    """
    original_file = tmpdir.join("original.txt")
    copied_file = tmpdir.join("copied.txt")
    output_file = tmpdir.join("output.txt")
    original_file.write("")
    copied_file.write("")
    main.main([original_file, copied_file, output_file])
    with open(output_file, 'r', encoding='utf-8') as f:
        assert f.read() == "0.00"


def test_main_identical_files(tmpdir):
    """
    测试 main 函数在处理完全相同文件时的情况。
    构造测试数据：创建两个内容相同的文件。
    """
    original_file = tmpdir.join("original.txt")
    copied_file = tmpdir.join("copied.txt")
    output_file = tmpdir.join("output.txt")
    original_file.write("这是一个测试句子")
    copied_file.write("这是一个测试句子")
    main.main([original_file, copied_file, output_file])
    with open(output_file, 'r', encoding='utf-8') as f:
        assert f.read() == "1.00"


def test_main_different_files(tmpdir):
    """
    测试 main 函数在处理完全不同文件时的情况。
    构造测试数据：创建两个内容不同的文件。
    """
    original_file = tmpdir.join("original.txt")
    copied_file = tmpdir.join("copied.txt")
    output_file = tmpdir.join("output.txt")
    original_file.write("这是一个测试句子")
    copied_file.write("这是另一个测试句子")
    main.main([original_file, copied_file, output_file])
    with open(output_file, 'r', encoding='utf-8') as f:
        similarity = float(f.read())
        assert 0 <= similarity < 1


def test_main_large_files(tmpdir):
    """
    测试 main 函数在处理大文件时的情况。
    构造测试数据：创建两个大文件。
    """
    original_file = tmpdir.join("original.txt")
    copied_file = tmpdir.join("copied.txt")
    output_file = tmpdir.join("output.txt")
    original_file.write("这是一个测试句子。" * 1000)
    copied_file.write("这是另一个测试句子。" * 1000)
    main.main([original_file, copied_file, output_file])
    with open(output_file, 'r', encoding='utf-8') as f:
        similarity = float(f.read())
        assert 0 <= similarity <= 1


def test_main_special_characters(tmpdir):
    """
    测试 main 函数在处理包含特殊字符的文件时的情况。
    构造测试数据：创建两个包含特殊字符的文件。
    """
    original_file = tmpdir.join("original.txt")
    copied_file = tmpdir.join("copied.txt")
    output_file = tmpdir.join("output.txt")
    original_file.write("这是一个测试句子！@#￥%……&*（）")
    copied_file.write("这是另一个测试句子！@#￥%……&*（）")
    main.main([original_file, copied_file, output_file])
    with open(output_file, 'r', encoding='utf-8') as f:
        similarity = float(f.read())
        assert 0 <= similarity <= 1