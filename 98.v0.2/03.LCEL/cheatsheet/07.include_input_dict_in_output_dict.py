from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)

runnable1 = RunnableLambda(lambda x: x["foo"] +7)

chain = RunnableParallel(bar=runnable1, baz=RunnablePassthrough())

print(chain.invoke({"foo": 10}))
# {'bar': 17, 'baz': {'foo': 10}}