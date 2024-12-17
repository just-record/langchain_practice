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

print(chain.invoke(7, config={"max_concurrency": 2}))