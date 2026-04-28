from utils.config_handler import prompt_config
from utils.path_tool import get_abs_path
from utils.logger_handler import logger

# 加载系统提示语
def load_system_prompt():
    try:
        system_prompt = get_abs_path(prompt_config["main_prompt_path"])

    except KeyError as e:
        logger.error(f"[加载系统提示语]错误: {e}")
        raise e # 抛出异常

    try:
        return open(system_prompt, "r", encoding="utf-8").read()

    except Exception as e:
        logger.error(f"[加载系统提示语]解析系统提示语错误: {str(e)}")
        raise e


# 加载rag提示语
def load_rag_prompt():
    try:
        rag_summarize_prompt = get_abs_path(prompt_config["rag_summarize_prompt_path"])
    except KeyError as e:
        logger.error(f"[加载rag提示语]错误: {e}")
        raise e  # 抛出异常

    try:
        return open(rag_summarize_prompt, "r", encoding="utf-8").read()

    except Exception as e:
        logger.error(f"[加载rag提示语]解析系统提示语错误: {str(e)}")
        raise e


# 加载生成报告提示词
def load_report_prompt():
    try:
        report_prompt = get_abs_path(prompt_config["report_prompt_path"])
    except KeyError as e:
        logger.error(f"[加载生成报告提示词]错误: {e}")
        raise e  # 抛出异常

    try:
        return open(report_prompt, "r", encoding="utf-8").read()

    except Exception as e:
        logger.error(f"[加载生成报告提示词]解析系统提示语错误: {str(e)}")
        raise e


if __name__ == '__main__':
    print(load_system_prompt())

