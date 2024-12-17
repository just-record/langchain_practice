from typing import Optional

from langchain_core.runnables import RunnableLambda


def func(main_arg: dict, other_arg: Optional[str] = None) -> dict:
    if other_arg:
        return {**main_arg, **{"foo": other_arg}}
    return main_arg


##################################################################################
### 1. 함수 테스트 - other_arg가 None인 경우
print('1.', '-' * 50)
##################################################################################
main_arg = {"bar": 1, "abc": 2}
print(func(main_arg))
# 1. --------------------------------------------------
# {'bar': 1, 'abc': 2}


##################################################################################
### 2. 함수 테스트 - other_arg가 None가 아닌 경우
print('2.', '-' * 50)
##################################################################################
main_arg = {"bar": 1, "abc": 2}
other_arg = "baz"
print(func(main_arg, other_arg=other_arg))
# 2. --------------------------------------------------
# {'bar': 1, 'abc': 2, 'foo': 'baz'}


##################################################################################
### 3. RunnableLambda에 default invocation args 추가
### Runnable.bind()
print('3.', '-' * 50)
##################################################################################
runnable1 = RunnableLambda(func)
bound_runnable1 = runnable1.bind(other_arg="bye")

print(bound_runnable1.invoke({"bar": "hello"}))
# 3. --------------------------------------------------
# {'bar': 'hello', 'foo': 'bye'}