from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool


@tool
def foo(x: int, config: RunnableConfig) -> int:
    """Sum x and a secret int"""
    return x + config["configurable"]["__top_secret_int"]


##################################################################################
### 1. RunnableConfig - 런타임에 특정값을 Runnable에 전달
print('1.', '-' * 50)
##################################################################################    
results = foo.invoke({"x": 5}, {"configurable": {"__top_secret_int": 2, "traced_key": "bar"}})
print(results)
# 1. --------------------------------------------------
# 7