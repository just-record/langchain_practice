from langchain_core.runnables import RunnableLambda, RunnableParallel


runnable1 = RunnableLambda(lambda x: {"foo": x})
runnable2 = RunnableLambda(lambda x: [x] * 2)
runnable3 = RunnableLambda(lambda x: str(x))

chain = RunnableParallel(first=runnable1, second=runnable2, third=runnable3)
configured_chain = chain.with_config(max_concurrency=2)

### 11.configure_runnable_execution.py과 다른 점
# chain.with_config로 설정값을 초기화 함. 따로 저장 할 수도 있음

print(configured_chain.invoke(7))
# {'first': {'foo': 7}, 'second': [7, 7], 'third': '7'}