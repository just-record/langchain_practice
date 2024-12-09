from langchain_core.runnables import RunnableLambda


def func(x):
    return x + 5


runnable = RunnableLambda(func)
print(runnable.invoke(2))
# 7