from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini")

#################################################################################
### 1. 이벤트 확인
### 
print('1.', '-' * 50)
##################################################################################
import asyncio

events = []
async def astream_events_func():
    async for event in model.astream_events("hello", version="v2"):
        events.append(event)
        
asyncio.run(astream_events_func())

rprint(events[:3])
print(' ')
rprint(events[-2:])
# 1. --------------------------------------------------
# [
#     {
#         'event': 'on_chat_model_start',
#         'data': {'input': 'hello'},
#         'name': 'ChatOpenAI',
#         'tags': [],
#         'run_id': '7055bc4b-c0c0-4df4-99f9-c130165b5c41',
#         'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7},
#         'parent_ids': []
#     },
#     {
#         'event': 'on_chat_model_stream',
#         'run_id': '7055bc4b-c0c0-4df4-99f9-c130165b5c41',
#         'name': 'ChatOpenAI',
#         'tags': [],
#         'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7},
#         'data': {'chunk': AIMessageChunk(content='', additional_kwargs={}, response_metadata={}, id='run-7055bc4b-c0c0-4df4-99f9-c130165b5c41')},
#         'parent_ids': []
#     },
#     {
#         'event': 'on_chat_model_stream',
#         'run_id': '7055bc4b-c0c0-4df4-99f9-c130165b5c41',
#         'name': 'ChatOpenAI',
#         'tags': [],
#         'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7},
#         'data': {'chunk': AIMessageChunk(content='Hello', additional_kwargs={}, response_metadata={}, id='run-7055bc4b-c0c0-4df4-99f9-c130165b5c41')},
#         'parent_ids': []
#     }
# ]
# 
# [
#     {
#         'event': 'on_chat_model_stream',
#         'run_id': '96738e7f-df1b-4786-a2a4-fed2a665ab13',
#         'name': 'ChatOpenAI',
#         'tags': [],
#         'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7},
#         'data': {
#             'chunk': AIMessageChunk(
#                 content='',
#                 additional_kwargs={},
#                 response_metadata={'finish_reason': 'stop', 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_6fc10e10eb'},
#                 id='run-96738e7f-df1b-4786-a2a4-fed2a665ab13'
#             )
#         },
#         'parent_ids': []
#     },
#     {
#         'event': 'on_chat_model_end',
#         'data': {
#             'output': AIMessageChunk(
#                 content='Hello! How can I assist you today?',
#                 additional_kwargs={},
#                 response_metadata={'finish_reason': 'stop', 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_6fc10e10eb'},
#                 id='run-96738e7f-df1b-4786-a2a4-fed2a665ab13'
#             )
#         },
#         'run_id': '96738e7f-df1b-4786-a2a4-fed2a665ab13',
#         'name': 'ChatOpenAI',
#         'tags': [],
#         'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7},
#         'parent_ids': []
#     }
# ]