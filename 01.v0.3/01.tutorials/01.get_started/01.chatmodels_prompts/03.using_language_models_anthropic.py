from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

# from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
### '.env' 파일에 'ANTHROPIC_API_KEY=sk-ant-...' API_KEY를 저장해야 함

##################################################################################
### 1. ChatAnthropic 모델 개체 생성 - Anthropic
print('1', '*'*50)
##################################################################################
model = ChatAnthropic(model="claude-3-5-sonnet-20240620")
rprint(model)
# 1 **************************************************
# ChatAnthropic(model='claude-3-5-sonnet-20240620', anthropic_api_url='https://api.anthropic.com', anthropic_api_key=SecretStr('**********'), model_kwargs={})

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
#     additional_kwargs={},
#     response_metadata={
#         'id': 'msg_018kud6DMfnSsBuAZNZKtyQd',
#         'model': 'claude-3-5-sonnet-20240620',
#         'stop_reason': 'end_turn',
#         'stop_sequence': None,
#         'usage': {'input_tokens': 17, 'output_tokens': 7}
#     },
#     id='run-b47b29f4-8a4a-4ef4-b892-c22f78338cf5-0',
#     usage_metadata={'input_tokens': 17, 'output_tokens': 7, 'total_tokens': 24, 'input_token_details': {}}
# )


##################################################################################
### 3. Streaming
print('3', '*'*50)
##################################################################################
for token in model.stream(messages):
    print(token.content, end="|")
# 3 **************************************************
# |안녕하세요! (|Annyeonghaseyo!)||