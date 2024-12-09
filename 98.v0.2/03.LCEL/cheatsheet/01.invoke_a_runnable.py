from langchain_core.runnables import RunnableLambda

runnable = RunnableLambda(lambda x: str(x))
print(f'type runnable: {type(runnable)}')
# type runnable: <class 'langchain_core.runnables.base.RunnableLambda'>
print(runnable.invoke(5))
# 5

### 비동기 실행
# import asyncio
# from langchain_core.runnables import RunnableLambda

# async def main():
#     runnable = RunnableLambda(lambda x: str(x))
#     result = await runnable.ainvoke(5)
#     print(result)

# asyncio.run(main())