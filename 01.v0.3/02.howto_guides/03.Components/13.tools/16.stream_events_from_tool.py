from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


model = ChatOpenAI(model="gpt-4o-mini")

### 긴 문장을 10 words 이하로 요하하고 결과를 뒤집어 반환
@tool
async def special_summarization_tool(long_text: str) -> str:
    """A tool that summarizes input text using advanced techniques."""
    prompt = ChatPromptTemplate.from_template(
        "You are an expert writer. Summarize the following text in 10 words or less:\n\n{long_text}"
    )

    def reverse(x: str):
        return x[::-1]

    chain = prompt | model | StrOutputParser() | reverse
    summary = await chain.ainvoke({"long_text": long_text})
    return summary


#################################################################################
### 1. 도구 호출 - 긴문장 -> 10 words 이하로 요약 -> 결과 뒤집어 반환
print('1.', '-' * 50)
################################################################################## 
LONG_TEXT = """
NARRATOR:
(Black screen with text; The sound of buzzing bees can be heard)
According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don't care what humans think is impossible.
BARRY BENSON:
(Barry is picking out a shirt)
Yellow, black. Yellow, black. Yellow, black. Yellow, black. Ooh, black and yellow! Let's shake it up a little.
JANET BENSON:
Barry! Breakfast is ready!
BARRY:
Coming! Hang on a second.
"""

async def ainvoke_func():
    return await special_summarization_tool.ainvoke({"long_text": LONG_TEXT})

import asyncio
rprint(asyncio.run(ainvoke_func()))
# 1. --------------------------------------------------
# .trihs lufroloc ni tsafkaerb rof seraperp ;scisyhp seifed eeB


#################################################################################
### 2. astream_events 확인
### Python 3.10.12 이어서 이벤트 발생 하지 않음
print('2.', '-' * 50)
################################################################################## 
stream = special_summarization_tool.astream_events(
    {"long_text": LONG_TEXT}, version="v2"
)

async def print_stream(stream) -> None:
    async for event in stream:
        if event["event"] == "on_chat_model_end":
            # Never triggers in python<=3.10!
            rprint(event)

asyncio.run(print_stream(stream))   
### Python 3.11 이상 버전을 사용하지 않는 경우, 이벤트가 발생하지 않습니다. ###         
### Python 3.10.12 이어서 이벤트 발생하지 않음
########################################################
### 아래는 공식문서 내용 그대로
########################################################
# {
#     'event': 'on_chat_model_end', 
#     'data': 
#         {
#             'output': AIMessage(
#                 content='Bee defies physics; Barry chooses outfit for graduation day.', 
#                 response_metadata={'stop_reason': 'end_turn', 'stop_sequence': None}, 
#                 id='run-d23abc80-0dce-4f74-9d7b-fb98ca4f2a9e', 
#                 usage_metadata={'input_tokens': 182, 'output_tokens': 16, 'total_tokens': 198}), 
#             'input': {
#                 'messages': [
#                     [HumanMessage(content="You are an expert writer. Summarize the following text in 10 words or less:\n\n\nNARRATOR:\n(Black screen with text; The sound of buzzing bees can be heard)\nAccording to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don't care what humans think is impossible.\nBARRY BENSON:\n(Barry is picking out a shirt)\nYellow, black. Yellow, black. Yellow, black. Yellow, black. Ooh, black and yellow! Let's shake it up a little.\nJANET BENSON:\nBarry! Breakfast is ready!\nBARRY:\nComing! Hang on a second.\n")]
#                 ]
#             }
#         }, 
#     'run_id': 'd23abc80-0dce-4f74-9d7b-fb98ca4f2a9e', 
#     'name': 'ChatAnthropic', 
#     'tags': ['seq:step:2'], 
#     'metadata': {'ls_provider': 'anthropic', 'ls_model_name': 'claude-3-5-sonnet-20240620', 'ls_model_type': 'chat', 'ls_temperature': 0.0, 'ls_max_tokens': 1024}, 
#     'parent_ids': ['f25c41fe-8972-4893-bc40-cecf3922c1fa']
# }


#################################################################################
### 3. astream_events 확인
### 위의 예제가 내부 체인에 도구의 설정 객체를 전달하지 않기 때문입니다. 
### RunnableConfig로 타입이 지정된 특별한 매개변수를 받도록 도구를 재정의해야 합니다
print('3.', '-' * 50)
################################################################################## 
from langchain_core.runnables import RunnableConfig


@tool
async def special_summarization_tool_with_config(
    long_text: str, config: RunnableConfig
) -> str:
    """A tool that summarizes input text using advanced techniques."""
    # print(f'config: {config}')
    prompt = ChatPromptTemplate.from_template(
        "You are an expert writer. Summarize the following text in 10 words or less:\n\n{long_text}"
    )

    def reverse(x: str):
        return x[::-1]

    chain = prompt | model | StrOutputParser() | reverse
    # Pass the "config" object as an argument to any executed runnables
    summary = await chain.ainvoke({"long_text": long_text}, config=config)
    return summary

stream = special_summarization_tool_with_config.astream_events(
    {"long_text": LONG_TEXT}, version="v2"
)

async def print_stream(stream) -> None:
    async for event in stream:
        if event["event"] == "on_chat_model_end":
            # Never triggers in python<=3.10!
            rprint(event)

asyncio.run(print_stream(stream))
# 3. --------------------------------------------------
# {
#     'event': 'on_chat_model_end',
#     'data': {
#         'output': AIMessage(
#             content='Bee defies logic; prepares for breakfast with excitement.',
#             additional_kwargs={},
#             response_metadata={'finish_reason': 'stop', 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_0aa8d3e20b'},
#             id='run-424d744a-9368-4913-b5a6-57bc714492fb'
#         ),
#         'input': {
#             'messages': [
#                 [
#                     HumanMessage(
#                         content="You are an expert writer. Summarize the following text in 10 words or less:\n\n\nNARRATOR:\n(Black screen with text; The sound of buzzing bees can be heard)\nAccording to all 
# known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don't care what humans think
# is impossible.\nBARRY BENSON:\n(Barry is picking out a shirt)\nYellow, black. Yellow, black. Yellow, black. Yellow, black. Ooh, black and yellow! Let's shake it up a little.\nJANET BENSON:\nBarry! Breakfast is 
# ready!\nBARRY:\nComing! Hang on a second.\n",
#                         additional_kwargs={},
#                         response_metadata={}
#                     )
#                 ]
#             ]
#         }
#     },
#     'run_id': '424d744a-9368-4913-b5a6-57bc714492fb',
#     'name': 'ChatOpenAI',
#     'tags': ['seq:step:2'],
#     'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7},
#     'parent_ids': ['0553b65d-486f-48ec-af30-07b7df9b996f']
# }
        



#################################################################################
### 4. astream_events 확인
### 스트리밍의 경우, astream_events()는 가능한 경우 스트리밍이 활성화된 체인 내의 내부 실행 가능 항목들을 자동으로 호출합니다. 
### 따라서 채팅 모델에서 생성되는 토큰들의 스트림을 보고 싶다면, 다른 변경 없이 단순히 on_chat_model_stream 이벤트를 찾도록 필터링하기만 하면 됩니다.
print('4.', '-' * 50)
################################################################################## 
stream = special_summarization_tool_with_config.astream_events(
    {"long_text": LONG_TEXT}, version="v2"
)

async def print_stream(stream) -> None:
    async for event in stream:
        if event["event"] == "on_chat_model_stream":
            # Never triggers in python<=3.10!
            rprint(event)

asyncio.run(print_stream(stream))
# 4. --------------------------------------------------
# {
#     'event': 'on_chat_model_stream',
#     'data': {'chunk': AIMessageChunk(content='', additional_kwargs={}, response_metadata={}, id='run-2824e506-5d71-4577-b1b5-0a81732ce8c2')},
#     'run_id': '2824e506-5d71-4577-b1b5-0a81732ce8c2',
#     'name': 'ChatOpenAI',
#     'tags': ['seq:step:2'],
#     'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7},
#     'parent_ids': ['e2ea8f54-c179-4f3c-ba92-1d3b9174fc93']
# }
# {
#     'event': 'on_chat_model_stream',
#     'data': {'chunk': AIMessageChunk(content='Bee', additional_kwargs={}, response_metadata={}, id='run-2824e506-5d71-4577-b1b5-0a81732ce8c2')},
#     'run_id': '2824e506-5d71-4577-b1b5-0a81732ce8c2',
#     'name': 'ChatOpenAI',
#     'tags': ['seq:step:2'],
#     'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7},
#     'parent_ids': ['e2ea8f54-c179-4f3c-ba92-1d3b9174fc93']
# }
# {
#     'event': 'on_chat_model_stream',
#     'data': {'chunk': AIMessageChunk(content=' def', additional_kwargs={}, response_metadata={}, id='run-2824e506-5d71-4577-b1b5-0a81732ce8c2')},
#     'run_id': '2824e506-5d71-4577-b1b5-0a81732ce8c2',
#     'name': 'ChatOpenAI',
#     'tags': ['seq:step:2'],
#     'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7},
#     'parent_ids': ['e2ea8f54-c179-4f3c-ba92-1d3b9174fc93']
# }
# {
#     'event': 'on_chat_model_stream',
#     'data': {'chunk': AIMessageChunk(content='ies', additional_kwargs={}, response_metadata={}, id='run-2824e506-5d71-4577-b1b5-0a81732ce8c2')},
#     'run_id': '2824e506-5d71-4577-b1b5-0a81732ce8c2',
#     'name': 'ChatOpenAI',
#     'tags': ['seq:step:2'],
#     'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7},
#     'parent_ids': ['e2ea8f54-c179-4f3c-ba92-1d3b9174fc93']
# }
# {
#     'event': 'on_chat_model_stream',
#     'data': {'chunk': AIMessageChunk(content=' aviation', additional_kwargs={}, response_metadata={}, id='run-2824e506-5d71-4577-b1b5-0a81732ce8c2')},
#     'run_id': '2824e506-5d71-4577-b1b5-0a81732ce8c2',
#     'name': 'ChatOpenAI',
#     'tags': ['seq:step:2'],
#     'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7},
#     'parent_ids': ['e2ea8f54-c179-4f3c-ba92-1d3b9174fc93']
# }
# {
#     'event': 'on_chat_model_stream',
#     'data': {'chunk': AIMessageChunk(content=' laws', additional_kwargs={}, response_metadata={}, id='run-2824e506-5d71-4577-b1b5-0a81732ce8c2')},
#     'run_id': '2824e506-5d71-4577-b1b5-0a81732ce8c2',
#     'name': 'ChatOpenAI',
#     'tags': ['seq:step:2'],
#     'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7},
#     'parent_ids': ['e2ea8f54-c179-4f3c-ba92-1d3b9174fc93']
# }
# {
#     'event': 'on_chat_model_stream',
#     'data': {'chunk': AIMessageChunk(content=';', additional_kwargs={}, response_metadata={}, id='run-2824e506-5d71-4577-b1b5-0a81732ce8c2')},
#     'run_id': '2824e506-5d71-4577-b1b5-0a81732ce8c2',
#     'name': 'ChatOpenAI',
#     'tags': ['seq:step:2'],
#     'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7},
#     'parent_ids': ['e2ea8f54-c179-4f3c-ba92-1d3b9174fc93']
# }
# {
#     'event': 'on_chat_model_stream',
#     'data': {'chunk': AIMessageChunk(content=' prepares', additional_kwargs={}, response_metadata={}, id='run-2824e506-5d71-4577-b1b5-0a81732ce8c2')},
#     'run_id': '2824e506-5d71-4577-b1b5-0a81732ce8c2',
#     'name': 'ChatOpenAI',
#     'tags': ['seq:step:2'],
#     'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7},
#     'parent_ids': ['e2ea8f54-c179-4f3c-ba92-1d3b9174fc93']
# }
# {
#     'event': 'on_chat_model_stream',
#     'data': {'chunk': AIMessageChunk(content=' for', additional_kwargs={}, response_metadata={}, id='run-2824e506-5d71-4577-b1b5-0a81732ce8c2')},
#     'run_id': '2824e506-5d71-4577-b1b5-0a81732ce8c2',
#     'name': 'ChatOpenAI',
#     'tags': ['seq:step:2'],
#     'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7},
#     'parent_ids': ['e2ea8f54-c179-4f3c-ba92-1d3b9174fc93']
# }
# {
#     'event': 'on_chat_model_stream',
#     'data': {'chunk': AIMessageChunk(content=' breakfast', additional_kwargs={}, response_metadata={}, id='run-2824e506-5d71-4577-b1b5-0a81732ce8c2')},
#     'run_id': '2824e506-5d71-4577-b1b5-0a81732ce8c2',
#     'name': 'ChatOpenAI',
#     'tags': ['seq:step:2'],
#     'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7},
#     'parent_ids': ['e2ea8f54-c179-4f3c-ba92-1d3b9174fc93']
# }
# {
#     'event': 'on_chat_model_stream',
#     'data': {'chunk': AIMessageChunk(content='.', additional_kwargs={}, response_metadata={}, id='run-2824e506-5d71-4577-b1b5-0a81732ce8c2')},
#     'run_id': '2824e506-5d71-4577-b1b5-0a81732ce8c2',
#     'name': 'ChatOpenAI',
#     'tags': ['seq:step:2'],
#     'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7},
#     'parent_ids': ['e2ea8f54-c179-4f3c-ba92-1d3b9174fc93']
# }
# {
#     'event': 'on_chat_model_stream',
#     'data': {
#         'chunk': AIMessageChunk(
#             content='',
#             additional_kwargs={},
#             response_metadata={'finish_reason': 'stop', 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_0aa8d3e20b'},
#             id='run-2824e506-5d71-4577-b1b5-0a81732ce8c2'
#         )
#     },
#     'run_id': '2824e506-5d71-4577-b1b5-0a81732ce8c2',
#     'name': 'ChatOpenAI',
#     'tags': ['seq:step:2'],
#     'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7},
#     'parent_ids': ['e2ea8f54-c179-4f3c-ba92-1d3b9174fc93']
# }