from langchain_core.runnables import RunnableLambda, RunnableParallel

runnable1 = RunnableLambda(lambda x: {"foo": x})
runnable2 = RunnableLambda(lambda x: [x] * 2)

##################################################################################
### 1. 병렬로 Runnables invoke하기
print('1.', '-' * 50)
##################################################################################
chain = RunnableParallel(first=runnable1, second=runnable2)

print(chain.invoke(2))
# 1. --------------------------------------------------
# {'first': {'foo': 2}, 'second': [2, 2]}