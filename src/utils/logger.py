import logging
import sys
from pathlib import Path

def setup_logger(name: str, level: str = "DEBUG",
                log_file: str = None,
                console_output: bool = True,
                info_fmt: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s") -> logging.Logger:
    """配置日志器"""

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    formatter = logging.Formatter(info_fmt)

    # 添加控制台输出
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # 添加文件输出
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger