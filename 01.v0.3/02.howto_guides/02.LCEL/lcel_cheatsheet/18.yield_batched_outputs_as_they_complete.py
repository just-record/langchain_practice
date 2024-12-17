import time

from langchain_core.runnables import RunnableLambda, RunnableParallel

### 파이썬에서 or 연산자는 첫 번째 truthy 값을 반환하는 방식으로 동작 ###
### 아래 함수와 동일
# def func(x):
#     time.sleep(x)
#     print(f"slept {x}")
#     return None
runnable1 = RunnableLambda(lambda x: time.sleep(x) or print(f"slept {x}"))


##################################################################################
### 1. 배치 처리 작업을 수행할 때 작업이 완료되는 순서대로 결과를 받는 방법
### batch_as_completed: 여러 입력값([5, 1])을 배치로 처리, 작업이 완료되는 순서대로 결과를 yield
print('1.', '-' * 50)
##################################################################################
for idx, result in runnable1.batch_as_completed([5, 1]):
    print(idx, result)
# 1. --------------------------------------------------
# slept 1 => 1초 후 출력
# 1 None
# slept 5 => 5초 후 출력
# 0 None    


##################################################################################
### 2. 비동기 호출
print('2.', '-' * 50)
##################################################################################
async def afunc(x):
    async for idx, result in runnable1.abatch_as_completed([5, 1]):
        print(idx, result)
        
import asyncio
asyncio.run(afunc([5, 1]))
# 2. --------------------------------------------------
# slept 1 => 1초 후 출력
# 1 None
# slept 5 => 5초 후 출력
# 0 None  
