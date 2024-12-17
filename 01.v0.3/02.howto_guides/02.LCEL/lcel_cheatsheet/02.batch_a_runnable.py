from langchain.globals import set_debug, get_debug
set_debug(False)

from langchain_core.runnables import RunnableLambda

runnable = RunnableLambda(lambda x: str(x))

##################################################################################
### 1. Batch로 처리
print('1.', '-' * 50)
##################################################################################
print(runnable.batch([7, 8, 9]))
# ['7', '8', '9']

##################################################################################
### 2. 비동기 실행
### await 키워드를 사용하지 않은 경우: 비동기 객체(coroutine)가 실제로 실행되지 않고 대기 상태로 남게 됨
print('2.', '-' * 50)
##################################################################################
import asyncio

async def abatch_func():
    print(await runnable.abatch([7, 8, 9]))
    
asyncio.run(abatch_func())    
# 2. --------------------------------------------------
# ['7', '8', '9']