from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI

##################################################################################
### 1. ChatOpenAI로 모델 개체 생성 - OpenAI 
print('1', '*'*50)
##################################################################################
model = ChatOpenAI(model="gpt-4o-mini")
rprint(model)
# 1 **************************************************
# ChatOpenAI(
#     client=<openai.resources.chat.completions.Completions object at 0x7ceb4e1d5b40>,
#     async_client=<openai.resources.chat.completions.AsyncCompletions object at 0x7ceb4e1d7c40>,
#     root_client=<openai.OpenAI object at 0x7ceb51576650>,
#     root_async_client=<openai.AsyncOpenAI object at 0x7ceb4e1d5ba0>,
#     model_name='gpt-4o-mini',
#     model_kwargs={},
#     openai_api_key=SecretStr('**********')
# )

from langchain_core.messages import HumanMessage, SystemMessage

messages = [
    SystemMessage("Translate the following from English into Korean"),
    HumanMessage("hi!"),
]

##################################################################################
### 2. model invoke - OpenAI 
print('2', '*'*50)
##################################################################################
response = model.invoke(messages)
rprint(response)
# 2 **************************************************
# AIMessage(
#     content='안녕하세요!',
#     additional_kwargs={'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 3,
#             'prompt_tokens': 20,
#             'total_tokens': 23,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-mini-2024-07-18',
#         'system_fingerprint': 'fp_bba3c8e70b',
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-559ef419-648e-4a58-8eaa-2d6db5187ebe-0',
#     usage_metadata={'input_tokens': 20, 'output_tokens': 3, 'total_tokens': 23, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )


##################################################################################
### 3. Streaming
print('3', '*'*50)
##################################################################################
for token in model.stream(messages):
    print(token.content, end="|")
# 3 **************************************************
# |안|녕하세요|!||    