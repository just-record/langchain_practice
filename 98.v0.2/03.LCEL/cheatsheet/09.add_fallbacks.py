from langchain_core.runnables import RunnableLambda


runnable1 = RunnableLambda(lambda x: x + "foo")
runnable2 = RunnableLambda(lambda x: str(x) + "foo")

chain = runnable1.with_fallbacks([runnable2])

# runnable1의 결과가 str이 아니기 때문에 runnable2가 실행됩니다.
print(chain.invoke(10))
# 10foo
    