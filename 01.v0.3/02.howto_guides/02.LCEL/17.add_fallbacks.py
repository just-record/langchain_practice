from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI


from unittest.mock import patch

import httpx
from openai import RateLimitError

request = httpx.Request("GET", "/")
response = httpx.Response(200, request=request)
error = RateLimitError("rate limit", response=response, body="")


# Note that we set max_retries = 0 to avoid retrying on RateLimits, etc
openai_llm = ChatOpenAI(model="gpt-4o-mini", max_retries=0)
# openai_4o_llm = ChatOpenAI(model="gpt-4o")
anthropic_llm = ChatAnthropic(model="claude-3-haiku-20240307")
llm = openai_llm.with_fallbacks([anthropic_llm])


##################################################################################
### 1. Error 발생
print('1.', '-' * 50)
##################################################################################
# Let's use just the OpenAI LLm first, to show that we run into an error
with patch("openai.resources.chat.completions.Completions.create", side_effect=error):
    try:
        rprint(openai_llm.invoke("Why did the chicken cross the road?"))
    except RateLimitError:
        print("Hit error")
# Hit error        
        

##################################################################################
### 2. Error 발생 => Fallback to Anthropic
print('2.', '-' * 50)
##################################################################################
# Now let's try with fallbacks to Anthropic
with patch("openai.resources.chat.completions.Completions.create", side_effect=error):
    try:
        rprint(llm.invoke("Why did the chicken cross the road?"))
    except RateLimitError:
        print("Hit error")        
# AIMessage(
#     content='There are many classic and humorous answers to the age-old question "Why did the chicken cross the road?". Some common joke responses include:\n\n- To get to the other side\n- To prove to the possum it could be 
# done\n- It was the chicken\'s day off\n- Because it saw a delicious piece of bread on the other side\n- To demonstrate its superior mobility over the proverbial "why" \n\nThe joke is meant to be a simple, nonsensical question 
# that doesn\'t really have a serious answer. The humor comes from the various silly and unexpected responses people come up with. It\'s a classic riddle that is often used to elicit a laugh or start a lighthearted 
# conversation.',
#     additional_kwargs={},
#     response_metadata={
#         'id': 'msg_01E9qYth5LzAxWAMahEX8q8i',
#         'model': 'claude-3-haiku-20240307',
#         'stop_reason': 'end_turn',
#         'stop_sequence': None,
#         'usage': {'input_tokens': 15, 'output_tokens': 155, 'cache_creation_input_tokens': 0, 'cache_read_input_tokens': 0}
#     },
#     id='run-c7b05b6f-0354-47bd-9396-14a0296b95e5-0',
#     usage_metadata={'input_tokens': 15, 'output_tokens': 155, 'total_tokens': 170, 'input_token_details': {'cache_read': 0, 'cache_creation': 0}}
# )        


##################################################################################
### 3. normal LLM처럼 사용 가능
print('3.', '-' * 50)
##################################################################################
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You're a nice assistant who always includes a compliment in your response",
        ),
        ("human", "Why did the {animal} cross the road"),
    ]
)
chain = prompt | llm

with patch("openai.resources.chat.completions.Completions.create", side_effect=error):
    try:
        rprint(chain.invoke({"animal": "kangaroo"}))
    except RateLimitError:
        print("Hit error")
# 3. --------------------------------------------------
# AIMessage(
#     content="I don't actually know why the kangaroo crossed the road. That sounds like the setup for a joke, but without a punchline, I can't provide a definitive answer. However, I'm happy to engage in a lighthearted exchange
# and try to come up with a creative or amusing response, if you'd like. You seem to have a fun sense of humor, and I enjoy our witty banter.",
#     additional_kwargs={},
#     response_metadata={
#         'id': 'msg_01Bttq3qoKhPpmFEH96AS29r',
#         'model': 'claude-3-haiku-20240307',
#         'stop_reason': 'end_turn',
#         'stop_sequence': None,
#         'usage': {'input_tokens': 30, 'output_tokens': 92, 'cache_creation_input_tokens': 0, 'cache_read_input_tokens': 0}
#     },
#     id='run-ecb550e5-43a0-4927-9417-f0dbc928621f-0',
#     usage_metadata={'input_tokens': 30, 'output_tokens': 92, 'total_tokens': 122, 'input_token_details': {'cache_read': 0, 'cache_creation': 0}}
# )        


##################################################################################
### 4. 시퀀스의 Fallback
### ChatOpenAI와 일반 OpenAI(채팅 모델을 사용하지 않음)라는 두 가지 다른 모델
print('4.', '-' * 50)
##################################################################################
# First let's create a chain with a ChatModel
# We add in a string output parser here so the outputs between the two are the same type
from langchain_core.output_parsers import StrOutputParser

chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You're a nice assistant who always includes a compliment in your response",
        ),
        ("human", "Why did the {animal} cross the road"),
    ]
)
# Here we're going to use a bad model name to easily create a chain that will error
chat_model = ChatOpenAI(model="gpt-fake")
bad_chain = chat_prompt | chat_model | StrOutputParser()


# Now lets create a chain with the normal OpenAI model
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

prompt_template = """Instructions: You should always include a compliment in your response.

Question: Why did the {animal} cross the road?"""
prompt = PromptTemplate.from_template(prompt_template)
llm = OpenAI()
good_chain = prompt | llm


# We can now create a final chain which combines the two
chain = bad_chain.with_fallbacks([good_chain])
results = chain.invoke({"animal": "turtle"})
rprint(results)
# 4. --------------------------------------------------


# Response: I'm not sure, but I must say that turtles are such resilient and determined creatures. I admire their perseverance.


##################################################################################
### 5. 긴 입력의 Fallback
### 컨텍스트 윈도우 - 일반적으로 LLM에 프롬프트를 보내기 전에 프롬프트의 길이를 계산하고 추적하지만 이것이 어렵거나 복잡한 상황
print('5.', '-' * 50)
##################################################################################
short_llm = ChatOpenAI()
long_llm = ChatOpenAI(model="gpt-4o-mini")
llm = short_llm.with_fallbacks([long_llm])

inputs = "What is the next number: " + ", ".join(["one", "two"] * 3000)

try:
    print(short_llm.invoke(inputs))
except Exception as e:
    print(e)
# 5. --------------------------------------------------
# Error code: 400 - {'error': {'message': "Sorry! We've encountered an issue with repetitive patterns in your prompt. Please try again with a different prompt.", 'type': 'invalid_request_error', 'param': 'prompt', 'code': 'invalid_prompt'}}    
    
try:
    rprint(llm.invoke(inputs))
except Exception as e:
    print(e)   
# AIMessage(
#     content='The next number in the sequence is "one." The sequence alternates between "one" and "two" repeatedly, and since it ends with "two," the next number will be "one."',
#     additional_kwargs={'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 41,
#             'prompt_tokens': 12012,
#             'total_tokens': 12053,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 11776}
#         },
#         'model_name': 'gpt-4o-mini-2024-07-18',
#         'system_fingerprint': 'fp_d02d531b47',
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-70156cf5-1357-45c4-bafd-b490107fde53-0',
#     usage_metadata={'input_tokens': 12012, 'output_tokens': 41, 'total_tokens': 12053, 'input_token_details': {'audio': 0, 'cache_read': 11776}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )     
    
    
##################################################################################
### 6. 더 나은 모델로의 Fallback
### 특정 형식(예: JSON)으로 출력하도록 요청 ->  GPT-3.5로 먼저 시도해보고(더 빠르고 저렴함), 파싱이 실패하면 GPT-4
### 3.5 모델의 성능이 향상되어 에러가 발생 하지 않음
print('6.', '-' * 50)
##################################################################################    
from langchain.output_parsers import DatetimeOutputParser

prompt = ChatPromptTemplate.from_template(
    "what time was {event} (in %Y-%m-%dT%H:%M:%S.%fZ format - only return this value)"
)

# In this case we are going to do the fallbacks on the LLM + output parser level
# Because the error will get raised in the OutputParser
openai_35 = ChatOpenAI() | DatetimeOutputParser()
openai_4 = ChatOpenAI(model="gpt-4o-mini") | DatetimeOutputParser()

only_35 = prompt | openai_35
fallback_4 = prompt | openai_35.with_fallbacks([openai_4])

try:
    print(only_35.invoke({"event": "the superbowl in 1994"}))
except Exception as e:
    print(f"Error: {e}")
# 6. --------------------------------------------------
# 1994-01-30 18:30:00    
    
    
try:
    print(fallback_4.invoke({"event": "the superbowl in 1994"}))
except Exception as e:
    print(f"Error: {e}")    
# 1994-01-30 15:30:00    