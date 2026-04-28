from typing import Callable

from langchain.agents import AgentState
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain.tools.tool_node import ToolCallRequest
from langchain_core.messages import ToolMessage
from langgraph.runtime import Runtime
from langgraph.types import Command
from utils.logger_handler import logger
from utils.prompt_loader import load_report_prompt,load_system_prompt

@wrap_tool_call
def monitor_tool(
        # 请求的数据封装
        request: ToolCallRequest,
        # 执行的函数本身
        handler: Callable[[ToolCallRequest],ToolMessage | Command]
) -> ToolMessage | Command: # 工具执行的监控

    logger.info(f"[工具调用]工具调用: {request.tool_call["name"]}")
    logger.info(f"[工具调用]工具调用参数: {request.tool_call['args']}")
    try:
        result = handler(request)
        logger.info(f"[工具调用]工具调用成功: {request.tool_call["name"]}")

        if request.tool_call["name"] == "fill_context_for_report":
            request.runtime.context["report"] = True

        return result
    except Exception as e:
        logger.error(f"[工具调用]工具调用异常:  {request.tool_call["name"]},原因: {str(e)}")
        raise e

@before_model
def log_before_model(
        state: AgentState, # 整个Agent智能体中的状态记录
        runtime: Runtime # 记录了整个执行过程中的上下文信息
): # 模型执行前的日志
    logger.info(f"[模型执行]模型执行即将执行, 带有{len(state["messages"])}条消息")
    logger.debug(
        f"[模型执行]{type(state['messages'][-1]).__name__}模型执行内容: {state['messages'][-1].content.strip()}")
    return None

@dynamic_prompt # 每一次在生成提示词之前, 调用这个函数
def report_prompt_switch(request: ModelRequest): # 生成报告提示词的切换, request: 是有langchain自动传入的
    is_report = request.runtime.context.get("report", False)
    if is_report:
        # 报告生成场景, 返回报告生成提示词内容
        return load_report_prompt()

    return load_system_prompt()
