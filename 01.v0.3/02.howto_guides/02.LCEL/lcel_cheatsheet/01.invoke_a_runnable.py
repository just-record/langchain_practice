from langchain_core.runnables import RunnableLambda
from rich import print as rprint

##################################################################################
### 1. RunnableLambda로 Runnable 생성
print('1.', '-' * 50)
##################################################################################
runnable = RunnableLambda(lambda x: str(x))
print(f'type runnable: {type(runnable)}')
# 1. --------------------------------------------------
# type runnable: <class 'langchain_core.runnables.base.RunnableLambda'>
print(' ')
print(runnable.invoke(5))
# 5

##################################################################################
### 2. 비동기 실행
print('2.', '-' * 50)
##################################################################################
import asyncio
from langchain_core.runnables import RunnableLambda

async def main():
    runnable = RunnableLambda(lambda x: str(x))
    result = await runnable.ainvoke(5)
    print(result)

asyncio.run(main())
# 2. --------------------------------------------------
# 5