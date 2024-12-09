from langchain_core.runnables import RunnableLambda, RunnablePassthrough


runnable1 = RunnableLambda(lambda x: x["foo"] + 7)

chain = RunnablePassthrough.assign(bar=runnable1)

print(chain.invoke({"foo": 10}))
# {'foo': 10, 'bar': 17}

### assign 메소드의 역할:
# 기존 입력에 새로운 키-값 쌍을 추가합니다.
# 이때 값은 다른 Runnable의 결과가 될 수 있습니다.


### assign 추가 테스트
print('-' * 30)
runnable2 = RunnableLambda(lambda x: x["foo"] * 2)
chain2 = RunnablePassthrough.assign(bar=runnable1).assign(baz=runnable2)
print(chain2.invoke({"foo": 10}))