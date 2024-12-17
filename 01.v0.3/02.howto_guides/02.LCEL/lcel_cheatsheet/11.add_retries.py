from langchain_core.runnables import RunnableLambda

counter = -1


def func(x):
    global counter
    counter += 1
    print(f"attempt with {counter=}")
    return x / counter


##################################################################################
### 1. 실패한 작업을 재시도(retry) 하기
### Runnable.with_retry()를 사용하여 작업을 재시도
### stop_after_attempt=2 를 사용하여 최대 2번까지 재시도
print('1.', '-' * 50)
##################################################################################
chain = RunnableLambda(func).with_retry(stop_after_attempt=2)

print(chain.invoke(2))
# 1. --------------------------------------------------
# attempt with counter=0
# attempt with counter=1
# 2.0