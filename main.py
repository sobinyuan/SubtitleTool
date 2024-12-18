import argparse
from src.core.splitter import SubtitleSplitter
from src.utils.logger import setup_logger

logger = setup_logger("main")

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='字幕智能断句工具')
    parser.add_argument('input', help='输入字幕文件路径')
    parser.add_argument('-o', '--output', help='输出字幕文件路径(可选)')
    args = parser.parse_args()

    try:
        # 初始化断句器
        splitter = SubtitleSplitter()

        # 测试API连接
        logger.info("正在测试API连接...")
        if not splitter.test_api():
            raise Exception("API连接测试失败，请检查配置")

        # 处理字幕
        output_path = splitter.process_subtitle(args.input, args.output)
        logger.info(f"处理完成！输出文件：{output_path}")

    except Exception as e:
        logger.error(f"处理失败: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()