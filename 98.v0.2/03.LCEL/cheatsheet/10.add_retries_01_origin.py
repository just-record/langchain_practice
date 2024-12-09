from langchain_core.runnables import RunnableLambda

counter = -1


def func(x):
    global counter
    counter += 1
    print(f"attempt with {counter=}")
    return x / counter


chain = RunnableLambda(func).with_retry(stop_after_attempt=2)

### with_retry: 주로 일시적인 오류나 예외가 발생했을 때 자동으로 재시도
# 오류 발생 시: 지정된 횟수만큼 재시도
# 오류가 없는 경우: 재시도하지 않고 결과를 즉시 반환

print(chain.invoke(2))