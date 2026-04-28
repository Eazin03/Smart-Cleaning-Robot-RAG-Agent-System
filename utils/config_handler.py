"""
配置文件处理
yaml -> k : v

"""

import yaml

from utils.path_tool import get_abs_path

# 加载和rag相关的配置文件
def load_rag_config(
        config_path:str = get_abs_path('config/rag.yml'),
        encoding:str = 'utf-8'
):
    with open(config_path, encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader) # 读取并解析yml文件，返回Python字典


# 加载和chroma相关的配置文件
def load_chroma_config(
        config_path: str = get_abs_path('config/chroma.yml'),
        encoding: str = 'utf-8'
):
    with open(config_path, encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader) # 读取并解析yml文件，返回Python字典


# 加载和prompts相关的配置文件
def load_prompts_config(
        config_path: str = get_abs_path('config/prompts.yml'),
        encoding: str = 'utf-8'
):
    with open(config_path, encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)  # 读取并解析yml文件，返回Python字典

# 加载和agent相关的配置文件
def load_agent_config(
        config_path: str = get_abs_path('config/agent.yml'),
        encoding: str = 'utf-8'
):
    with open(config_path, encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)  # 读取并解析yml文件，返回Python字典

rag_config = load_rag_config()
chroma_config = load_chroma_config()
prompt_config = load_prompts_config()
agent_config = load_agent_config()

if __name__ == '__main__':
    print(rag_config["chat_model_name"])
    print(prompt_config["main_prompt_path"])