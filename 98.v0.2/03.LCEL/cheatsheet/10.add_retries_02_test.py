from langchain_core.runnables import RunnableLambda


counter = 0

def func(x):
    global counter
    counter += 1
    print(f"attempt with {counter=}")
    # return x / counter
    return x / 0


## 1. stop_after_attempt에 의해 2번 재시도 하고 오류 발생
chain = RunnableLambda(func).with_retry(stop_after_attempt=2)

try:
    print(chain.invoke(2))
except Exception as e:
    print(e)
# attempt with counter=1
# attempt with counter=2
# division by zero    


### 2. retry_if_exception_type를 사용 하여 Exception Type을 지정하여 재시도
# 아래 코드는 ZeroDivisionError가 발생하는데 retry_if_exception_type에 해당 Exception이 없어서 재시도 하지 않음
print('-' * 50)
counter = 0
chain = RunnableLambda(func).with_retry(retry_if_exception_type=(ValueError, ConnectionError), stop_after_attempt=2)

try:
    print(chain.invoke(2))
except Exception as e:
    print(e)    
# attempt with counter=1
# division by zero