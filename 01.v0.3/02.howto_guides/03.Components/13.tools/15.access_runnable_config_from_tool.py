# pip install -qU langchain_core

from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool


@tool
async def reverse_tool(text: str, special_config_param: RunnableConfig) -> str:
    """A test tool that combines input text with a configurable parameter."""
    return (text + special_config_param["configurable"]["additional_field"])[::-1]


#################################################################################
### 1. 도구 호출은 기본적으로 병렬로 실행됨
### 'parallel_tool_call'을 사용 하여 단일 도구를 실행
print('1.', '-' * 50)
################################################################################## 
async def ainvoke_func():
    return await reverse_tool.ainvoke(
        {"text": "abc"}, config={"configurable": {"additional_field": "123"}}
    )
    
import asyncio
rprint(asyncio.run(ainvoke_func()))    
# 1. --------------------------------------------------
# 321cba
