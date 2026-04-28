from langchain.agents import create_agent
from model.factory import chat_model
from utils.prompt_loader import load_system_prompt
from agent.tool.agent_tools import (rag_summarize,get_weather,get_user_id,get_user_location,
                                    get_current_month,fetch_external_data,fill_context_for_report)
from agent.tool.middleware import monitor_tool,report_prompt_switch,log_before_model


class ReactAgent:
    """
    ReactAgent: 智能代理类
    """
    def __init__(self):
        self.agent = create_agent(
            model = chat_model,
            system_prompt= load_system_prompt(),
            tools= [rag_summarize,get_weather,get_user_id,get_user_location,
                    get_current_month,fetch_external_data,fill_context_for_report],
            middleware= [monitor_tool,report_prompt_switch,log_before_model]
        )

    def execute_stream(self,query):
        input_dict = {
            "messages": [
                {"role": "user", "content": query}
            ]
        }

        # 第三个参数context就是上下文runtime中的信息, 就是我们做提示词切换的标记
        for chunk in self.agent.stream(input_dict,stream_mode="values",context={"report": False}):
            lastest_message = chunk["messages"][-1]
            yield lastest_message.content.strip() + "\n"

if __name__ == '__main__':
    agent = ReactAgent()
    for chunk in agent.execute_stream("给我生成我的使用报告"):
        print(chunk,end="",flush=True)
