from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
import asyncio

model = ChatOpenAI(model="gpt-4o-mini")

#################################################################################
### 1. Chain 이벤트 확인
### 2개아 아닌 3개의 서로 다른 시작 이벤트 -> 체인, 모델, 파서
print('1.', '-' * 50)
##################################################################################
chain = (
    model | JsonOutputParser()
)  

import asyncio

events = []
async def astream_events_func():
    async for event in model.astream_events(
        "output a list of the countries france, spain and japan and their populations in JSON format. "
        'Use a dict with an outer key of "countries" which contains a list of countries. '
        "Each country should have the key `name` and `population`",
        version="v2",        
    ):
        events.append(event)
        
asyncio.run(astream_events_func())

rprint(events[:3])
# 1. --------------------------------------------------
# [
#     {
#         'event': 'on_chat_model_start',
#         'data': {
#             'input': 'output a list of the countries france, spain and japan and their populations in JSON format. Use a dict with an outer key of "countries" which contains a list of 
# countries. Each country should have the key `name` and `population`'
#         },
#         'name': 'ChatOpenAI',
#         'tags': [],
#         'run_id': '3963e2d3-cd0e-4b1f-97ec-700f60173b76',
#         'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7},
#         'parent_ids': []
#     },
#     {
#         'event': 'on_chat_model_stream',
#         'run_id': '3963e2d3-cd0e-4b1f-97ec-700f60173b76',
#         'name': 'ChatOpenAI',
#         'tags': [],
#         'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7},
#         'data': {'chunk': AIMessageChunk(content='', additional_kwargs={}, response_metadata={}, id='run-3963e2d3-cd0e-4b1f-97ec-700f60173b76')},
#         'parent_ids': []
#     },
#     {
#         'event': 'on_chat_model_stream',
#         'run_id': '3963e2d3-cd0e-4b1f-97ec-700f60173b76',
#         'name': 'ChatOpenAI',
#         'tags': [],
#         'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7},
#         'data': {'chunk': AIMessageChunk(content='Here', additional_kwargs={}, response_metadata={}, id='run-3963e2d3-cd0e-4b1f-97ec-700f60173b76')},
#         'parent_ids': []
#     }
# ]


#################################################################################
### 2. 모델과 파서의 스트림 이벤트 출력
### 모델과 파서의 스트림 이벤트를 출력하는 API를 사용 (시작 이벤트, 종료 이벤트, 체인의 이벤트는 무시합니다.)
### 모델과 파서는 모두 스트리밍을 지원하므로 이벤트를 실시간으로 출력할 수 있습니다.
print('2.', '-' * 50)
##################################################################################
num_events = 0

async def astream_events_func():
    async for event in chain.astream_events(
        "output a list of the countries france, spain and japan and their populations in JSON format. "
        'Use a dict with an outer key of "countries" which contains a list of countries. '
        "Each country should have the key `name` and `population`",
        version="v2",
    ):
        kind = event["event"]
        if kind == "on_chat_model_stream":
            print(
                f"Chat model chunk: {repr(event['data']['chunk'].content)}",
                flush=True,
            )
        if kind == "on_parser_stream":
            print(f"Parser chunk: {event['data']['chunk']}", flush=True)
        global num_events
        num_events += 1
        if num_events > 30:
            # Truncate the output
            print("...")
            break
        
asyncio.run(astream_events_func())
# 2. --------------------------------------------------
# Chat model chunk: ''
# Chat model chunk: 'Here'
# Chat model chunk: ' is'
# Chat model chunk: ' the'
# Chat model chunk: ' requested'
# Chat model chunk: ' data'
# Chat model chunk: ' in'
# Chat model chunk: ' JSON'
# Chat model chunk: ' format'
# Chat model chunk: ':\n\n'
# Chat model chunk: '```'
# Chat model chunk: 'json'
# Chat model chunk: '\n'
# Chat model chunk: '{\n'
# Parser chunk: {}
# Chat model chunk: ' '
# Chat model chunk: ' "'
# Chat model chunk: 'countries'
# Chat model chunk: '":'
# Chat model chunk: ' [\n'
# Parser chunk: {'countries': []}
# Chat model chunk: '   '
# Chat model chunk: ' {\n'
# Parser chunk: {'countries': [{}]}
# Chat model chunk: '     '
# ...