from langchain_core.runnables import RunnableLambda, RunnableParallel

runnable1 = RunnableLambda(lambda x: {"foo": x})
runnable2 = RunnableLambda(lambda x: [x] * 2)
runnable3 = RunnableLambda(lambda x: str(x))


##################################################################################
### 1. Runnable 객체들의 실행을 구성하고 제어하는 방법
### config={"max_concurrency": 2} => 최대 동시 실행 수를 2로 제한, 3개 중 2개만 동시 실행
### 12.configure_runnable_execution.py 와의 차이점 비교
### Chain 에 적용, Chain 을 다음에 호출할 때도 적용됨
print('1.', '-' * 50)
##################################################################################
chain = RunnableParallel(first=runnable1, second=runnable2, third=runnable3)
configured_chain = chain.with_config(max_concurrency=2)

# print(chain.invoke(7))  ### 아래 코드가 아닐까? 공식 문서의 예제가 잘못된 것 같다.
print(configured_chain.invoke(7))



##################################################################################
### 2. time을 두어 실제 호출 되는 시점을 확인
print('2.', '-' * 50)
##################################################################################
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
configured_chain = chain.with_config(max_concurrency=2)

print(configured_chain.invoke(7))
# 2. --------------------------------------------------
# function1 is running
# function2 is running
# function3 is running
# {'first': {'foo': 7}, 'second': [7, 7], 'third': '7'}


##################################################################################
### 3. config 없이 실행
print('3.', '-' * 50)
##################################################################################
print(configured_chain.invoke(7))
# 3. --------------------------------------------------
# function1 is running
# function2 is running
# function3 is running
# {'first': {'foo': 7}, 'second': [7, 7], 'third': '7'}

### 2개가 먼저 동시에 실행되고 1개는 그 다음에 실행됨 ###