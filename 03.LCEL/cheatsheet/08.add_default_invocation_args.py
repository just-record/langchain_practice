from langchain_core.runnables import RunnableLambda


def func(main_arg: dict, other_arg: str | None = None) -> dict:
    if other_arg:
        return {**main_arg, **{"foo": other_arg}}
    return main_arg

### func test
# othre_art is None
main_arg = {"bar": 1, "abc": 2}
print(func(main_arg))

# othre_art is not None
main_arg = {"bar": 1, "abc": 2}
other_arg = "baz"
print(func(main_arg, other_arg=other_arg))

print('-' * 30)

### add default invocation args
runnable1 = RunnableLambda(func)
bound_runnable1 = runnable1.bind(other_arg="bye")


### bind
# Runnable 객체에 부분적으로 인자를 미리 지정하기

print(bound_runnable1.invoke({"bar": "hello"}))
# {'bar': 'hello', 'foo': 'bye'}
