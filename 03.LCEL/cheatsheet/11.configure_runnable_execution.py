from langchain_core.runnables import RunnableLambda, RunnableParallel


runnable1 = RunnableLambda(lambda x: {"foo": x})
runnable2 = RunnableLambda(lambda x: [x] * 2)
runnable3 = RunnableLambda(lambda x: str(x))

chain = RunnableParallel(first=runnable1, second=runnable2, third=runnable3)

print(chain.invoke(7, config={"max_concurrency": 2}))

### config: Runnable 객체의 실행 방식을 세부적으로 조정. 다양한 실행 매개변수를 동적으로 설정.
# config의 인자는 Runnable 객체의 타입에 따라 다름. 각 Runnable 타입은 자신만의 특정 config 옵션을 가짐.
# max_concurrency: 병렬로 실행할 최대 작업 수: runnable1, runnable2, runnable3 중 2개의 작업이 병렬로 실행 된 후 나머지 1개의 작업이 실행됩니다.


# {'first': {'foo': 7}, 'second': [7, 7], 'third': '7'}