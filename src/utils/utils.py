import re

def is_mainly_cjk(text: str) -> bool:
    """
    判断文本是否主要由中日韩文字组成

    Args:
        text: 输入文本
    Returns:
        bool: 如果CJK字符占比超过50%则返回True
    """
    # 定义CJK字符的Unicode范围
    cjk_patterns = [
        r'[\u4e00-\u9fff]',           # 中日韩统一表意文字
        r'[\u3040-\u309f]',           # 平假名
        r'[\u30a0-\u30ff]',           # 片假名
        r'[\uac00-\ud7af]',           # 韩文音节
    ]

    # 计算CJK字符数
    cjk_count = 0
    for pattern in cjk_patterns:
        cjk_count += len(re.findall(pattern, text))

    # 计算总字符数（不包括空白字符）
    total_chars = len(''.join(text.split()))

    # 如果CJK字符占比超过50%，则认为主要是CJK文本
    return cjk_count / total_chars > 0.5 if total_chars > 0 else False

