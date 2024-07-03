from typing import Any

from langchain_core.runnables import (
    ConfigurableField,
    RunnableConfig,
    RunnableSerializable,
)


class FooRunnable(RunnableSerializable[dict, dict]):
    output_key: str

    def invoke(
        self, input: Any, config: RunnableConfig | None = None, **kwargs: Any
    ) -> list:
        return self._call_with_config(self.subtract_seven, input, config, **kwargs)

    def subtract_seven(self, input: dict) -> dict:
        return {self.output_key: input["foo"] - 7}


runnable1 = FooRunnable(output_key="bar")
configurable_runnable1 = runnable1.configurable_fields(
    output_key=ConfigurableField(id="output_key")
)

### 1. 'output_key'를 'not bar'로 설정
print(configurable_runnable1.invoke(
    {"foo": 10}, config={"configurable": {"output_key": "not bar"}}
))
# {'not bar': 3}

### 2. 'output_key'를 설정하지 않으면 기본값인 'bar'로 설정
print('-' * 50)
print(configurable_runnable1.invoke({"foo": 10}))
# {'bar': 3}