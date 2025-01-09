from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

import random
from typing import List, Tuple

from langchain_core.tools import tool

#################################################################################
### 1. Invoking the tool with ToolCall
### 도구 정의 - random int 생성 ###
### response_format="content_and_artifact" - 결과를 content와 artifact로 반환 ###
#################################################################################
@tool(response_format="content_and_artifact")
def generate_random_ints(min: int, max: int, size: int) -> Tuple[str, List[int]]:
    """Generate size random ints in the range [min, max]."""
    array = [random.randint(min, max) for _ in range(size)]
    content = f"Successfully generated array of {size} random ints in [{min}, {max}]."
    return content, array


#################################################################################
### 1-1. tool arguments 로만 직접 invoke => content만 반환
print('1-1.', '-' * 50)
################################################################################## 
rprint(generate_random_ints.invoke({"min": 0, "max": 9, "size": 10}))
# 1. --------------------------------------------------
# Successfully generated array of 10 random ints in [0, 9].


#################################################################################
### 1-2. ToolCall (dictionary - "name", "args", "id" , "type") invoke => content와 artifact 반환
print('1-2.', '-' * 50)
################################################################################## 
results = generate_random_ints.invoke(
    {
        "name": "generate_random_ints",
        "args": {"min": 0, "max": 9, "size": 10},
        "id": "123",  # required
        "type": "tool_call",  # required
    }
)
rprint(results)
# 2. --------------------------------------------------
# ToolMessage(content='Successfully generated array of 10 random ints in [0, 9].', name='generate_random_ints', tool_call_id='123', artifact=[7, 2, 3, 2, 0, 5, 2, 1, 2, 3])


#################################################################################
### 2. Using with a model
### tool-calling model로 Tool 호출과 ToolMessage 생성
#################################################################################
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools([generate_random_ints])

#################################################################################
### 2-1. 모델이 Tool을 호출 할 수 있는 ToolCall 생성
print('2-1.', '-' * 50)
################################################################################## 
ai_msg = llm_with_tools.invoke("generate 6 positive ints less than 25")
rprint(ai_msg.tool_calls)
# 2-1. --------------------------------------------------
# [{'name': 'generate_random_ints', 'args': {'min': 1, 'max': 24, 'size': 6}, 'id': 'call_tnULjsyNnYX08SvFfVGD3aBB', 'type': 'tool_call'}]

#################################################################################
### 2-2. Tool call 실행
print('2-2.', '-' * 50)
################################################################################## 
rprint(generate_random_ints.invoke(ai_msg.tool_calls[0]))
# 2-2. --------------------------------------------------
# ToolMessage(content='Successfully generated array of 6 random ints in [1, 24].', name='generate_random_ints', tool_call_id='call_fSK2ojALpIPXi8YrhxLZKEnx', artifact=[1, 5, 23, 4, 21, 4])

### tool call의 args만 전달하면 content만 반환 ###
print(' ')
rprint(generate_random_ints.invoke(ai_msg.tool_calls[0]["args"]))
# Successfully generated array of 6 random ints in [1, 24].


#################################################################################
### 2-3. chaining
print('2-3.', '-' * 50)
################################################################################## 
from operator import attrgetter

chain = llm_with_tools | attrgetter("tool_calls") | generate_random_ints.map()

rprint(chain.invoke("give me a random number between 1 and 5"))
# 2-3. --------------------------------------------------
# [ToolMessage(content='Successfully generated array of 1 random ints in [1, 5].', name='generate_random_ints', tool_call_id='call_NI5FDFYAlrhdq4wq4EBD1U1R', artifact=[3])]

### chaining을 단계 별로 확인 ###
print(' ')
results1 = llm_with_tools.invoke("give me a random number between 1 and 5")
rprint(results1)
# AIMessage(
#     content='',
#     additional_kwargs={'tool_calls': [{'id': 'call_iWxGty8hbBrTvAn3RkbI31V7', 'function': {'arguments': '{"min":1,"max":5,"size":1}', 'name': 'generate_random_ints'}, 'type': 'function'}], 'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 25,
#             'prompt_tokens': 70,
#             'total_tokens': 95,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-mini-2024-07-18',
#         'system_fingerprint': 'fp_f2cd28694a',
#         'finish_reason': 'tool_calls',
#         'logprobs': None
#     },
#     id='run-4d523dea-285c-4621-8c42-a51b95faab2d-0',
#     tool_calls=[{'name': 'generate_random_ints', 'args': {'min': 1, 'max': 5, 'size': 1}, 'id': 'call_iWxGty8hbBrTvAn3RkbI31V7', 'type': 'tool_call'}],
#     usage_metadata={'input_tokens': 70, 'output_tokens': 25, 'total_tokens': 95, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )

print(' ')
tool_calls_getter = attrgetter("tool_calls")
results2 = tool_calls_getter(results1)
rprint(results2)
# [{'name': 'generate_random_ints', 'args': {'min': 1, 'max': 5, 'size': 1}, 'id': 'call_iWxGty8hbBrTvAn3RkbI31V7', 'type': 'tool_call'}]

print(' ')
results3 = generate_random_ints.map().invoke(results2)
rprint(results3)
# [ToolMessage(content='Successfully generated array of 1 random ints in [1, 5].', name='generate_random_ints', tool_call_id='call_iWxGty8hbBrTvAn3RkbI31V7', artifact=[2])]


#################################################################################
### 3. Creating from BaseTool class
### BaseTool을 상속 받아 BaseTool 개체를 직접 생성 하기
#################################################################################
from langchain_core.tools import BaseTool


class GenerateRandomFloats(BaseTool):
    name: str = "generate_random_floats"
    description: str = "Generate size random floats in the range [min, max]."
    response_format: str = "content_and_artifact"

    ndigits: int = 2

    def _run(self, min: float, max: float, size: int) -> Tuple[str, List[float]]:
        range_ = max - min
        array = [
            round(min + (range_ * random.random()), ndigits=self.ndigits)
            for _ in range(size)
        ]
        content = f"Generated {size} floats in [{min}, {max}], rounded to {self.ndigits} decimals."
        return content, array

    # Optionally define an equivalent async method

    # async def _arun(self, min: float, max: float, size: int) -> Tuple[str, List[float]]:
    #     ...
    
    
#################################################################################
### 3-1. tool arguments 로만 직접 invoke => content만 반환
print('3-1.', '-' * 50)
##################################################################################     
rand_gen = GenerateRandomFloats(ndigits=4)
rprint(rand_gen.invoke({"min": 0.1, "max": 3.3333, "size": 3}))
# 3-1. --------------------------------------------------
# Generated 3 floats in [0.1, 3.3333], rounded to 4 decimals.


#################################################################################
### 3-2. ToolCall (dictionary - "name", "args", "id" , "type") invoke => content와 artifact 반환
print('3-2.', '-' * 50)
##################################################################################     
results = rand_gen.invoke(
    {
        "name": "generate_random_floats",
        "args": {"min": 0.1, "max": 3.3333, "size": 3},
        "id": "123",
        "type": "tool_call",
    }
)
rprint(results)
# 3-2. --------------------------------------------------
# ToolMessage(content='Generated 3 floats in [0.1, 3.3333], rounded to 4 decimals.', name='generate_random_floats', tool_call_id='123', artifact=[2.5994, 1.1728, 1.1626])