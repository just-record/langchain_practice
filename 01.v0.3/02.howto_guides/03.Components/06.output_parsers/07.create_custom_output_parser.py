from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint


#################################################################################
### 1. Runnable Lambdas and Generators - 파서 생성
### 모델의 출력 대소문자를 반전시키는 간단한 파서
print('1.', '-' * 50)
##################################################################################
from typing import Iterable

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, AIMessageChunk

model = ChatOpenAI(model_name="gpt-4o")


def parse(ai_message: AIMessage) -> str:
    """Parse the AI message."""
    return ai_message.content.swapcase()


chain = model | parse
rprint(chain.invoke("hello"))
# 1. --------------------------------------------------
# hELLO! hOW CAN i ASSIST YOU TODAY?


#################################################################################
### 2. Runnable Lambdas and Generators - stream 확인
print('2.', '-' * 50)
##################################################################################
for chunk in chain.stream("tell me about yourself in one sentence"):
    print(chunk, end="|", flush=True)
# 2. --------------------------------------------------
# i'M AN ai LANGUAGE MODEL DESIGNED TO ASSIST WITH A WIDE RANGE OF QUESTIONS AND TASKS BY PROVIDING INFORMATION, GENERATING TEXT, AND OFFERING SUPPORT ACROSS VARIOUS TOPICS.|
### streaming 안 됨 ###
### 파서가 출력을 파싱하기 전에 입력을 집계 ###


#################################################################################
### 3. Runnable Lambdas and Generators - streaming 가능한 파서 생성
### 파서가 입력에 대한 반복자(iterable)를 받아들이고 결과를 사용 가능할 때마다 yield 하기
print('3.', '-' * 50)
##################################################################################
from langchain_core.runnables import RunnableGenerator


def streaming_parse(chunks: Iterable[AIMessageChunk]) -> Iterable[str]:
    for chunk in chunks:
        yield chunk.content.swapcase()


streaming_parse = RunnableGenerator(streaming_parse)
chain = model | streaming_parse
rprint(chain.invoke("hello"))
# 3. --------------------------------------------------
# hELLO! hOW CAN i ASSIST YOU TODAY?


### streaming 확인 ###
print(' ')
for chunk in chain.stream("tell me about yourself in one sentence"):
    print(chunk, end="|", flush=True)
# |i'M| AN| ai| LANGUAGE| MODEL| DESIGNED| TO| ASSIST| WITH| A| WIDE| RANGE| OF| INQUIRIES| BY| PROVIDING| INFORMATION|,| ANSWERING| QUESTIONS|,| AND| GENERATING| TEXT| BASED| ON| THE| INPUT| i| RECEIVE|.||    