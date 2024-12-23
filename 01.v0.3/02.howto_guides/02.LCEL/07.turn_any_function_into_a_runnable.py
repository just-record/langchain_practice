from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint


from operator import itemgetter

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI


def length_function(text):
    return len(text)


def _multiple_length_function(text1, text2):
    return len(text1) * len(text2)


def multiple_length_function(_dict):
    return _multiple_length_function(_dict["text1"], _dict["text2"])


model = ChatOpenAI()

prompt = ChatPromptTemplate.from_template("what is {a} + {b}")

##################################################################################
### 1. Using the constructor
### RunnableLambda 생성자를 사용하여 우리의 커스텀 로직을 명시적으로 래핑
print('1.', '-' * 50)
##################################################################################
# chain1 = prompt | model

chain = (
    {
        "a": itemgetter("foo") | RunnableLambda(length_function),
        "b": {"text1": itemgetter("foo"), "text2": itemgetter("bar")}
        | RunnableLambda(multiple_length_function),
    }
    | prompt
    | model
)

results = chain.invoke({"foo": "bar", "bar": "gah"})
rprint(results.content)
# 1. --------------------------------------------------
# 3 + 9 equals 12.


##################################################################################
### 2. The convenience @chain decorator
### @chain 데코레이터는 custom_chain을 runnable로 변환
print('2.', '-' * 50)
##################################################################################
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import chain

prompt1 = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
prompt2 = ChatPromptTemplate.from_template("What is the subject of this joke: {joke}")


@chain
def custom_chain(text):
    prompt_val1 = prompt1.invoke({"topic": text})
    output1 = ChatOpenAI().invoke(prompt_val1)
    parsed_output1 = StrOutputParser().invoke(output1)
    chain2 = prompt2 | ChatOpenAI() | StrOutputParser()
    return chain2.invoke({"joke": parsed_output1})


results = custom_chain.invoke("bears")
rprint(results)
# 2. --------------------------------------------------
# The subject of the joke is the bear.


##################################################################################
### 3. Automatic coercion in chains
### 자동 형변환(coercion)을 활용
print('3.', '-' * 50)
##################################################################################
prompt = ChatPromptTemplate.from_template("tell me a story about {topic}")

model = ChatOpenAI()

chain_with_coerced_function = prompt | model | (lambda x: x.content[:5])

results = chain_with_coerced_function.invoke({"topic": "bears"})
rprint(results)
# 3. --------------------------------------------------
# 'Once '


##################################################################################
### 4. Passing run metadata
### Runnable 람다는 선택적으로 RunnableConfig 매개변수를 받을 수 있음
print('4.', '-' * 50)
##################################################################################
import json

from langchain_core.runnables import RunnableConfig


# text: JSON 형식이어야 하는 문자열
# config: 실행 설정 정보를 담은 객체
def parse_or_fix(text: str, config: RunnableConfig):
    # 잘못된 JSON을 수정하기 위한 체인
    fixing_chain = (
        # LLM에게 텍스트를 수정하도록 요청하는 프롬프트
        ChatPromptTemplate.from_template(
            "Fix the following text:\n\n\`\`\`text\n{input}\n\`\`\`\nError: {error}"
            " Don't narrate, just respond with the fixed data."
        )
        | model
        | StrOutputParser()
    )
    for _ in range(3): # 최대 3번 시도
        try:
            return json.loads(text) # JSON 파싱 시도
        except Exception as e: # 파싱 실패시
            text = fixing_chain.invoke({"input": text, "error": e}, config) # 에러 정보와 함께 LLM에 전달
    return "Failed to parse"


from langchain_community.callbacks import get_openai_callback

# API 호출 횟수, 토큰 사용량 등을 추적하기 위한 콜백 생성
with get_openai_callback() as cb:
    output = RunnableLambda(parse_or_fix).invoke(
        "{foo: bar}", {"tags": ["my-tag"], "callbacks": [cb]}
    )
    print(output)
    print(cb)
# 잘못된 JSON 입력: {foo: bar}
# json.loads()로 파싱 시도 → 실패
# LLM에게 수정 요청: "foo"를 따옴표로 감싸도록 수정
# 수정된 텍스트로 다시 파싱 시도
# 성공하면 파싱된 JSON 반환, 실패하면 다시 시도 (최대 3번)    

# 4. --------------------------------------------------
# {'foo': 'bar'}
# Tokens Used: 71
#         Prompt Tokens: 61
#         Completion Tokens: 10
# Successful Requests: 1
# Total Cost (USD): $4.55e-05    
    

##################################################################################
### 5. Streaming
### 스트리밍을 지원해야 하는 경우 RunnableGenerator(yield 키워드를 사용하고 반복자처럼 동작하는 함수)를 사용
print('5.', '-' * 50)
##################################################################################
from typing import Iterator, List

prompt = ChatPromptTemplate.from_template(
    "Write a comma-separated list of 5 animals similar to: {animal}. Do not include numbers"
)

str_chain = prompt | model | StrOutputParser()

for chunk in str_chain.stream({"animal": "bear"}):
    print(chunk, end="", flush=True)
# 5. --------------------------------------------------
# lion, tiger, wolf, gorilla, raccoon    


##################################################################################
### 6. Streaming - 스트리밍에 사용자 정의 함수 적용 하기
### 현재 스트리밍된 출력을 집계하고 모델이 목록의 다음 쉼표를 생성할 때 그것을 산출하는 사용자 정의 함수를 정의
print('6.', '-' * 50)
##################################################################################
# This is a custom parser that splits an iterator of llm tokens
# into a list of strings separated by commas
def split_into_list(input: Iterator[str]) -> Iterator[List[str]]:
    # hold partial input until we get a comma
    buffer = ""
    for chunk in input:
        # add current chunk to buffer
        buffer += chunk
        # while there are commas in the buffer
        while "," in buffer:
            # split buffer on comma
            comma_index = buffer.index(",")
            # yield everything before the comma
            yield [buffer[:comma_index].strip()]
            # save the rest for the next iteration
            buffer = buffer[comma_index + 1 :]
    # yield the last chunk
    yield [buffer.strip()]


list_chain = str_chain | split_into_list

for chunk in list_chain.stream({"animal": "bear"}):
    print(chunk, flush=True)
# 6. --------------------------------------------------
# ['lion']
# ['tiger']
# ['wolf']
# ['gorilla']
# ['panda']    


##################################################################################
### 7. Streaming - 위 코드의 비동기 버전
print('7.', '-' * 50)
##################################################################################
from typing import AsyncIterator


async def asplit_into_list(
    input: AsyncIterator[str],
) -> AsyncIterator[List[str]]:  # async def
    buffer = ""
    async for (
        chunk
    ) in input:  # `input` is a `async_generator` object, so use `async for`
        buffer += chunk
        while "," in buffer:
            comma_index = buffer.index(",")
            yield [buffer[:comma_index].strip()]
            buffer = buffer[comma_index + 1 :]
    yield [buffer.strip()]


list_chain = str_chain | asplit_into_list

async def astream_func():
    async for chunk in list_chain.astream({"animal": "bear"}):
        print(chunk, flush=True)
        
import asyncio
asyncio.run(astream_func())
# 7. --------------------------------------------------
# ['lion']
# ['tiger']
# ['wolf']
# ['gorilla']
# ['panda']