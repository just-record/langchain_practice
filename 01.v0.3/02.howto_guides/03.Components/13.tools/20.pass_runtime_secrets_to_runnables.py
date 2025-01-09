from rich import print as rprint
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool


#################################################################################
### 1. Runnables에 secret을 전달하는 방법
### 런너블(Runnable)을 실행할 때 RunnableConfig를 사용하여 비밀값을 전달
### configurable 필드에 __ 접두사를 붙여 비밀값을 전달
### 이렇게 하면 이러한 비밀값들이 실행 과정에서 추적되지 않도록 보장됩니다.
print('1.', '-' * 50)
#################################################################################
@tool
def foo(x: int, config: RunnableConfig) -> int:
    """Sum x and a secret int"""
    return x + config["configurable"]["__top_secret_int"]


rprint(foo.invoke({"x": 5}, {"configurable": {"__top_secret_int": 2, "traced_key": "bar"}}))
# 1. --------------------------------------------------
# 7


# "추적되지 않는다"는 것은 실행 로그나 모니터링 시스템에서 해당 값이 기록되지 않는다는 의미

# __ 접두사가 없는 일반적인 configurable 값들 (예: traced_key: "bar")은:

# 실행 로그에 기록됨
# 디버깅 출력에 표시됨
# 모니터링 시스템에서 볼 수 있음


# __ 접두사가 있는 비밀값들 (예: __top_secret_int: 2)은:

# 실행 로그에서 제외됨
# 디버깅 출력에서 숨겨짐
# 모니터링 시스템에서 마스킹 처리됨