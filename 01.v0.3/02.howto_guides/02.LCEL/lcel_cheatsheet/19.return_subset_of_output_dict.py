from langchain_core.runnables import RunnableLambda, RunnablePassthrough

runnable1 = RunnableLambda(lambda x: x["baz"] + 5)
chain = RunnablePassthrough.assign(foo=runnable1).pick(["foo", "bar"])


##################################################################################
### 1. 딕셔너리의 특정 키들만 선택적으로 출력하는 방법
### .pick(["foo", "bar"]): 결과 딕셔너리에서 "foo"와 "bar" 키만 선택
print('1.', '-' * 50)
##################################################################################
print(chain.invoke({"bar": "hi", "baz": 2}))
# 1. --------------------------------------------------
# {'foo': 7, 'bar': 'hi'}