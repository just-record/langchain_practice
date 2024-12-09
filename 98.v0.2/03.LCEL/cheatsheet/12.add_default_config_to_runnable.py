from langchain_core.runnables import RunnableLambda, RunnableParallel
import time

def function1(x):
    print("function1 is running")
    time.sleep(1)
    return {"foo": x}

def function2(x):
    print("function2 is running")
    time.sleep(1)
    return [x] * 2

def function3(x):
    print("function3 is running")
    time.sleep(1)
    return str(x)

runnable1 = RunnableLambda(function1)
runnable2 = RunnableLambda(function2)
runnable3 = RunnableLambda(function3)

chain = RunnableParallel(first=runnable1, second=runnable2, third=runnable3)
### 1. with_config()
print(chain.with_config(max_concurrency=2).invoke(7))
# {'first': {'foo': 7}, 'second': [7, 7], 'third': '7'}


### 2. 새로운 chain으로 저장 가능
print('-'*30)
configured_chain = chain.with_config(max_concurrency=2)
print(configured_chain.invoke(7))
# {'first': {'foo': 7}, 'second': [7, 7], 'third': '7'}


### 11.configure_runnable_execution.py과 다른 점
# chain.with_config로 설정값을 초기화 함. 따로 저장 할 수도 있음