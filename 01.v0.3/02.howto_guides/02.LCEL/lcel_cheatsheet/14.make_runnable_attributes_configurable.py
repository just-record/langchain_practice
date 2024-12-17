from typing import Any, Optional

from langchain_core.runnables import (
    ConfigurableField,
    RunnableConfig,
    RunnableSerializable,
)


class FooRunnable(RunnableSerializable[dict, dict]):
    output_key: str

    def invoke(
        self, input: Any, config: Optional[RunnableConfig] = None, **kwargs: Any
    ) -> list:
        return self._call_with_config(self.subtract_seven, input, config, **kwargs)

    def subtract_seven(self, input: dict) -> dict:
        return {self.output_key: input["foo"] - 7}


##################################################################################
### 1. Runnable 객체의 속성을 동적으로 설정
### configurable_fields를 사용해 output_key를 동적 설정 가능하게 만듦
print('1.', '-' * 50)
##################################################################################
runnable1 = FooRunnable(output_key="bar")
configurable_runnable1 = runnable1.configurable_fields(
    output_key=ConfigurableField(id="output_key")
)


results = configurable_runnable1.invoke(
    {"foo": 10}, config={"configurable": {"output_key": "not bar"}}
)
print(results)
# 1. --------------------------------------------------
# {'not bar': 3}


##################################################################################
### 2. Runnable 객체의 속성을 동적으로 설정
### configurable_fields를 설정 하지 않음
print('2.', '-' * 50)
##################################################################################
results = configurable_runnable1.invoke({"foo": 10})
print(results)
# 2. --------------------------------------------------
# {'bar': 3}