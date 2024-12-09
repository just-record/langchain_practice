from langchain_core.runnables import RunnableLambda

runnable1 = RunnableLambda(lambda x: {"foo": x})
runnable2 = RunnableLambda(lambda x: [x] * 2)

chain = runnable1 | runnable2

print(chain.invoke(2))
# [{'foo': 2}, {'foo': 2}]