from langchain_core.runnables import RunnableLambda, RunnablePassthrough

runnable1 = RunnableLambda(lambda x: x["baz"] + 5)
# 'foo'와 'bar'만 반환 - 'baz'는 반환하지 않음
chain = RunnablePassthrough.assign(foo=runnable1).pick(["foo", "bar"])

print(chain.invoke({"bar": "hi", "baz": 2}))
# {'foo': 7, 'bar': 'hi'}