from langchain_core.runnables import RunnableLambda, RunnableParallel

runnable1 = RunnableLambda(lambda x: {"foo": x})
runnable2 = RunnableLambda(lambda x: [x] * 2)

chain = RunnableLambda(lambda x: runnable1 if x > 6 else runnable2)

### 1. input 값이 6보다 크면 runnable1을 실행
print(chain.invoke(7))
# {'foo': 7}

### 2. input 값이 6보다 작으면 runnable2를 실행
print('-' * 50)
print(chain.invoke(5))
# [5, 5]
