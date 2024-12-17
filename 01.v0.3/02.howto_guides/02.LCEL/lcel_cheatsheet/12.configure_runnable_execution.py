from langchain_core.runnables import RunnableLambda, RunnableParallel

runnable1 = RunnableLambda(lambda x: {"foo": x})
runnable2 = RunnableLambda(lambda x: [x] * 2)
runnable3 = RunnableLambda(lambda x: str(x))

##################################################################################
### 1. Runnable 객체들의 실행을 구성하고 제어하는 방법
### config={"max_concurrency": 2} => 최대 동시 실행 수를 2로 제한, 3개 중 2개만 동시 실행
### 호출 시 config 매개변수를 사용하여 한번 만 적용, Chain 객체에 영구적으로 적용되지 않음
print('1.', '-' * 50)
##################################################################################
chain = RunnableParallel(first=runnable1, second=runnable2, third=runnable3)

print(chain.invoke(7, config={"max_concurrency": 2}))
# 1. --------------------------------------------------
# {'first': {'foo': 7}, 'second': [7, 7], 'third': '7'}


### config: Runnable 객체의 실행 방식을 세부적으로 조정 ### 
### 다양한 실행 매개변수를 동적으로 설정
### config의 인자는 Runnable 객체의 타입에 따라 다름 
### 각 Runnable 타입은 자신만의 특정 config 옵션을 가짐


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

print(chain.invoke(7, config={"max_concurrency": 2}))
# 2. --------------------------------------------------
# function1 is running
# function2 is running
# function3 is running
# {'first': {'foo': 7}, 'second': [7, 7], 'third': '7'}


##################################################################################
### 3. config 없이 실행
print('3.', '-' * 50)
##################################################################################
print(chain.invoke(7))
# 3. --------------------------------------------------
# function1 is running
# function2 is running
# function3 is running
# {'first': {'foo': 7}, 'second': [7, 7], 'third': '7'}

### 한꺼번에 실행됨 ###