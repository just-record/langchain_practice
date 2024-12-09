from langchain_core.runnables import RunnableLambda
import time


def func(x):
    for y in x:
        print(f'y: {y}')
        yield str(y)


runnable = RunnableLambda(func)


for chunk in runnable.stream(range(5)):
    time.sleep(0.3)
    print(chunk)

# y: 0
# 0
# y: 1
# 1
# y: 2
# 2
# y: 3
# 3
# y: 4
# 4

# Async variant:
# async for chunk in await runnable.astream(range(5)):
#     print(chunk)    