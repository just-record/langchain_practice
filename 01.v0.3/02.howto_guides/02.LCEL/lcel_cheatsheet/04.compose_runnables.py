from langchain_core.runnables import RunnableLambda

runnable1 = RunnableLambda(lambda x: {"foo": x})
runnable2 = RunnableLambda(lambda x: [x] * 2)

##################################################################################
### 1. Runnables 구성하기
print('1.', '-' * 50)
##################################################################################

chain = runnable1 | runnable2

print(chain.invoke(2))
# 1. --------------------------------------------------
# [{'foo': 2}, {'foo': 2}]