from langchain_core.runnables import RunnableLambda

runnable1 = RunnableLambda(lambda x: list(range(x)))
runnable2 = RunnableLambda(lambda x: x + 5)

##################################################################################
### 1. Runnable 객체의 배치 처리를 선언적으로 만드는 방법
### .map()은 runnable2를 리스트의 각 요소에 적용하도록 만듦
print('1.', '-' * 50)
##################################################################################
chain = runnable1 | runnable2.map()

print(chain.invoke(3))
# 1. --------------------------------------------------
# [5, 6, 7]