import os
from pathlib import Path
from typing import Optional
import openai
from dotenv import load_dotenv

from .merge_segments import merge_segments

from .asr_data import from_subtitle_file
from ..utils.logger import setup_logger

logger = setup_logger("subtitle_splitter")

class SubtitleSplitter:
    def __init__(self):
        load_dotenv()

        # 加载配置
        self.base_url = os.getenv('OPENAI_BASE_URL')
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('LLM_MODEL')
        self.thread_num = int(os.getenv('THREAD_NUM', '5'))
        self.batch_size = int(os.getenv('BATCH_SIZE', '10'))
        self.max_word_count_cjk = int(os.getenv('MAX_WORD_COUNT_CJK', '20'))
        self.max_word_count_english = int(os.getenv('MAX_WORD_COUNT_ENGLISH', '12'))

        # 验证必要配置
        if not all([self.base_url, self.api_key, self.model]):
            raise ValueError("请在.env文件中配置必要的API参数")

        # 设置OpenAI环境
        os.environ['OPENAI_BASE_URL'] = self.base_url
        os.environ['OPENAI_API_KEY'] = self.api_key

        # 初始化OpenAI客户端
        self.client = openai.OpenAI()

    def test_api(self) -> bool:
        """测试API连接"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                {"role": "system", "content": "You are a helpful assistant now."},
                {"role": "user", "content": "Hello!"}
            ],
            max_tokens=100,
            timeout=10
            )
            return True
        except Exception as e:
            logger.error(f"API测试失败: {str(e)}")
            return False

    def process_subtitle(self, input_path: str, output_path: Optional[str] = None) -> str:
        """处理字幕文件"""
        try:
            # 验证输入文件
            input_path = Path(input_path)
            if not input_path.exists():
                raise FileNotFoundError(f"输入文件不存在: {input_path}")
            if input_path.suffix not in ['.srt', '.vtt', '.ass']:
                raise ValueError(f"不支持的字幕格式: {input_path.suffix}")

            # 设置输出路径
            if output_path is None:
                output_path = str(input_path.parent / f"【智能断句】{input_path.stem}.srt")

            # 加载字幕文件
            logger.info(f"正在加载字幕文件: {input_path}")
            asr_data = from_subtitle_file(str(input_path))

            # 转换为逐字字幕
            if not asr_data.is_word_timestamp():
                logger.info("正在转换为逐字字幕...")
                asr_data.split_to_word_segments()

            # 智能断句
            if asr_data.is_word_timestamp():
                logger.info("正在进行智能断句...")
                asr_data = merge_segments(
                    asr_data,
                    model=self.model,
                    num_threads=self.thread_num,
                    max_word_count_cjk=self.max_word_count_cjk,
                    max_word_count_english=self.max_word_count_english
                )

            # 保存结果
            logger.info(f"正在保存断句结果: {output_path}")
            asr_data.save(save_path=output_path)

            return output_path

        except Exception as e:
            logger.exception("处理字幕文件失败")
            raise e