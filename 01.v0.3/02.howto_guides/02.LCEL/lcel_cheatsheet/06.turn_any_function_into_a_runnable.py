from langchain_core.runnables import RunnableLambda


def func(x):
    return x + 5

##################################################################################
### 1. 일반 함수를 Runnable으로 변환
print('1.', '-' * 50)
##################################################################################
runnable = RunnableLambda(func)
print(runnable.invoke(2))