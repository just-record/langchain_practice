from langchain_core.runnables import RunnableLambda

runnable = RunnableLambda(lambda x: str(x))
print(f'type runnable: {type(runnable)}')
# type runnable: <class 'langchain_core.runnables.base.RunnableLambda'>
print(runnable.invoke(5))
# 5

# Async variant:
# await runnable.ainvoke(5)