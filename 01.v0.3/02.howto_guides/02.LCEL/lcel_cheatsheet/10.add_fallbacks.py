from langchain_core.runnables import RunnableLambda

runnable1 = RunnableLambda(lambda x: x + "foo")
runnable2 = RunnableLambda(lambda x: str(x) + "foo")

##################################################################################
### 1. 작업이 실패 할 경우 대체 작업 실행하기
### Runnable.with_fallbacks()를 사용하여 대체 작업을 실행
print('1.', '-' * 50)
##################################################################################
chain = runnable1.with_fallbacks([runnable2])

print(chain.invoke(5))
# 1. --------------------------------------------------
# 5foo

##################################################################################
### 2. fallback 없이 실행
print('2.', '-' * 50)
##################################################################################
print(runnable1.invoke("5"))
# 2. --------------------------------------------------
# 5foo
print(' ')
print(runnable1.invoke(5))
# TypeError: unsupported operand type(s) for +: 'int' and 'str'