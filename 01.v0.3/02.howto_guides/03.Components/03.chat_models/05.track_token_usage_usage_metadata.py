from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

#################################################################################
### 1. Using AIMessage.usage_metadata - openai
print('1.', '-' * 50)
##################################################################################
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
openai_response = llm.invoke("hello")
rprint(openai_response.usage_metadata)
# 1. --------------------------------------------------
# {'input_tokens': 8, 'output_tokens': 10, 'total_tokens': 18, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}


#################################################################################
### 2. Using AIMessage.usage_metadata - anthropic
print('2.', '-' * 50)
##################################################################################
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-3-haiku-20240307")
anthropic_response = llm.invoke("hello")
rprint(anthropic_response.usage_metadata)
# 2. --------------------------------------------------
# {'input_tokens': 8, 'output_tokens': 12, 'total_tokens': 20, 'input_token_details': {'cache_read': 0, 'cache_creation': 0}}


#################################################################################
### 3. Using AIMessage.response_metadata - 업체마다 속성은 다름
print('3.', '-' * 50)
##################################################################################
print(f'OpenAI: {openai_response.response_metadata["token_usage"]}')
print(f'Anthropic: {anthropic_response.response_metadata["usage"]}')
# 3. --------------------------------------------------
# OpenAI: {'completion_tokens': 10, 'prompt_tokens': 8, 'total_tokens': 18, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}
# Anthropic: {'input_tokens': 8, 'output_tokens': 12, 'cache_creation_input_tokens': 0, 'cache_read_input_tokens': 0}


#################################################################################
### 4. 스트리밍 - openai는 스트리밍에서 token count를 제공 함
### stream_usage=True
print('4.', '-' * 50)
##################################################################################
llm = ChatOpenAI(model="gpt-4o-mini")

aggregate = None
for chunk in llm.stream("hello", stream_usage=True):
    print(chunk)
    aggregate = chunk if aggregate is None else aggregate + chunk
# 4. --------------------------------------------------
# content='' additional_kwargs={} response_metadata={} id='run-fa22889b-6828-4e66-bcb3-2beb3c1ad747'
# content='Hello' additional_kwargs={} response_metadata={} id='run-fa22889b-6828-4e66-bcb3-2beb3c1ad747'
# content='!' additional_kwargs={} response_metadata={} id='run-fa22889b-6828-4e66-bcb3-2beb3c1ad747'
# content=' How' additional_kwargs={} response_metadata={} id='run-fa22889b-6828-4e66-bcb3-2beb3c1ad747'
# content=' can' additional_kwargs={} response_metadata={} id='run-fa22889b-6828-4e66-bcb3-2beb3c1ad747'
# content=' I' additional_kwargs={} response_metadata={} id='run-fa22889b-6828-4e66-bcb3-2beb3c1ad747'
# content=' assist' additional_kwargs={} response_metadata={} id='run-fa22889b-6828-4e66-bcb3-2beb3c1ad747'
# content=' you' additional_kwargs={} response_metadata={} id='run-fa22889b-6828-4e66-bcb3-2beb3c1ad747'
# content=' today' additional_kwargs={} response_metadata={} id='run-fa22889b-6828-4e66-bcb3-2beb3c1ad747'
# content='?' additional_kwargs={} response_metadata={} id='run-fa22889b-6828-4e66-bcb3-2beb3c1ad747'
# content='' additional_kwargs={} response_metadata={'finish_reason': 'stop', 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_0aa8d3e20b'} id='run-fa22889b-6828-4e66-bcb3-2beb3c1ad747'
# content='' additional_kwargs={} response_metadata={} id='run-fa22889b-6828-4e66-bcb3-2beb3c1ad747' usage_metadata={'input_tokens': 8, 'output_tokens': 9, 'total_tokens': 17, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}    

print(' ')
print(aggregate.content)
print(aggregate.usage_metadata)
# Hello! How can I assist you today?
# {'input_tokens': 8, 'output_tokens': 9, 'total_tokens': 17, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}

### stream_usage=True 생략 하면 token count를 제공하지 않음 ###
print(' ')
aggregate = None
for chunk in llm.stream("hello"):
    print(chunk)
# content='' additional_kwargs={} response_metadata={} id='run-98f335cd-5d66-4cc2-bd1e-bbb869867bab'
# content='Hello' additional_kwargs={} response_metadata={} id='run-98f335cd-5d66-4cc2-bd1e-bbb869867bab'
# content='!' additional_kwargs={} response_metadata={} id='run-98f335cd-5d66-4cc2-bd1e-bbb869867bab'
# content=' How' additional_kwargs={} response_metadata={} id='run-98f335cd-5d66-4cc2-bd1e-bbb869867bab'
# content=' can' additional_kwargs={} response_metadata={} id='run-98f335cd-5d66-4cc2-bd1e-bbb869867bab'
# content=' I' additional_kwargs={} response_metadata={} id='run-98f335cd-5d66-4cc2-bd1e-bbb869867bab'
# content=' assist' additional_kwargs={} response_metadata={} id='run-98f335cd-5d66-4cc2-bd1e-bbb869867bab'
# content=' you' additional_kwargs={} response_metadata={} id='run-98f335cd-5d66-4cc2-bd1e-bbb869867bab'
# content=' today' additional_kwargs={} response_metadata={} id='run-98f335cd-5d66-4cc2-bd1e-bbb869867bab'
# content='?' additional_kwargs={} response_metadata={} id='run-98f335cd-5d66-4cc2-bd1e-bbb869867bab'
# content='' additional_kwargs={} response_metadata={'finish_reason': 'stop', 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_d02d531b47'} id='run-98f335cd-5d66-4cc2-bd1e-bbb869867bab'