# # | echo: false
# import nest_asyncio
# nest_asyncio.apply()

from langchain_core.runnables import RunnableLambda, RunnableParallel

runnable1 = RunnableLambda(lambda x: {"foo": x}, name="first")


async def func(x):
    for _ in range(5):
        yield x


runnable2 = RunnableLambda(func, name="second")

chain = runnable1 | runnable2


##################################################################################
### 1. 이벤트 스트림 생성
print('1.', '-' * 50)
##################################################################################
async def astream_events_func():
    async for event in chain.astream_events("bar", version="v2"):
        print(f"event={event['event']} | name={event['name']} | data={event['data']}")

import asyncio
asyncio.run(astream_events_func())
# 1. --------------------------------------------------
# event=on_chain_start | name=RunnableSequence | data={'input': 'bar'}
# event=on_chain_start | name=first | data={}
# event=on_chain_stream | name=first | data={'chunk': {'foo': 'bar'}}
# event=on_chain_start | name=second | data={}
# event=on_chain_end | name=first | data={'output': {'foo': 'bar'}, 'input': 'bar'}
# event=on_chain_stream | name=second | data={'chunk': {'foo': 'bar'}}
# event=on_chain_stream | name=RunnableSequence | data={'chunk': {'foo': 'bar'}}
# event=on_chain_stream | name=second | data={'chunk': {'foo': 'bar'}}
# event=on_chain_stream | name=RunnableSequence | data={'chunk': {'foo': 'bar'}}
# event=on_chain_stream | name=second | data={'chunk': {'foo': 'bar'}}
# event=on_chain_stream | name=RunnableSequence | data={'chunk': {'foo': 'bar'}}
# event=on_chain_stream | name=second | data={'chunk': {'foo': 'bar'}}
# event=on_chain_stream | name=RunnableSequence | data={'chunk': {'foo': 'bar'}}
# event=on_chain_stream | name=second | data={'chunk': {'foo': 'bar'}}
# event=on_chain_stream | name=RunnableSequence | data={'chunk': {'foo': 'bar'}}
# event=on_chain_end | name=second | data={'output': {'foo': 'bar'}, 'input': {'foo': 'bar'}}
# event=on_chain_end | name=RunnableSequence | data={'output': {'foo': 'bar'}}


### 주요 내용 ###

# 1. 두 개의 Runnable 객체를 생성합니다:
#    - `runnable1`: 입력값을 딕셔너리로 변환하는 동기 함수 (`{"foo": x}`)
#    - `runnable2`: 비동기 제너레이터 함수로, 입력값을 5번 반복해서 yield하는 함수

# 2. 파이프라인 연산자(`|`)를 사용해 두 runnable을 연결합니다:
#    - `runnable1`의 출력이 `runnable2`의 입력으로 전달됨

# 3. `astream_events()`를 사용해 이벤트 스트림을 생성:
#    - 비동기(async) 스트리밍 방식으로 이벤트를 처리
#    - `version="v2"` 파라미터로 이벤트 포맷 버전 지정

# 4. 출력되는 각 이벤트는 다음 정보를 포함:
#    - `event`: 이벤트 타입
#    - `name`: Runnable의 이름
#    - `data`: 실제 데이터 값