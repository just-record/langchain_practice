from langchain_core.runnables import RunnableLambda

runnable1 = RunnableLambda(lambda x: list(range(x)))
runnable2 = RunnableLambda(lambda x: x + 5)

chain = runnable1 | runnable2.map()

print(chain.invoke(3))
### map: 입력 컬렉션의 각 요소에 대해 Runnable을 실행합니다.
# runnable1 -> [0, 1, 2] => runnable2 -> [0, 1, 2]에 map 적용 -> [5, 6, 7] ===> 이런 느낌?
# [5, 6, 7]