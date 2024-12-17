from langchain_core.runnables import RunnableLambda


def func(x):
    for y in x:
        # print(f'y: {y}')
        yield str(y)


runnable = RunnableLambda(func)

##################################################################################
### 1. 스트림 하기
### 함수에서 yield를 사용하여 generator로 변경
print('1.', '-' * 50)
##################################################################################
for chunk in runnable.stream(range(5)):
    print(chunk)
# 1. --------------------------------------------------
# 0
# 1
# 2
# 3
# 4    


##################################################################################
### 2. 비동기 호출
### 오류가 발생한다. 잘 모르겠다.
### TypeError: Cannot stream from a generator function asynchronously.Use .stream() instead.
# print('2.', '-' * 50)
##################################################################################
# import asyncio

# async def astream_func():
#     # async for chunk in await runnable.astream(range(5)):
#     async for chunk in runnable.astream(range(5)):
#         # time.sleep(0.3)
#         print(chunk)
        
# asyncio.run(astream_func())        


##################################################################################
### 3. 스트림 불가능
### 함수에서 yield를 사용하지 않고 전체 결과를 반환
print('3.', '-' * 50)
##################################################################################
def func(x):
    return [str(y) for y in x]


runnable = RunnableLambda(func)

for chunk in runnable.stream(range(5)):
    print(chunk)
# 3. --------------------------------------------------
# ['0', '1', '2', '3', '4']    
