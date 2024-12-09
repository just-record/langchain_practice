from typing import Any, Optional

from langchain_core.runnables import (
    RunnableConfig, 
    RunnableLambda, 
    RunnableSerializable, 
    ConfigurableField
)



class ListRunnable(RunnableSerializable[Any, list]):
    def invoke(
        self, input: Any, config: RunnableConfig | None = None, **kwargs: Any
    ) -> list:
        return self._call_with_config(self.listify, input, config, **kwargs)

    def listify(self, input: Any) -> list:
        return [input]
    

class StrRunnable(RunnableSerializable[Any, str]):
    def invoke(
        self, input: Any, config: RunnableConfig | None = None, **kwargs: Any
    ) -> list:
        return self._call_with_config(self.strify, input, config, **kwargs)

    def strify(self, input: Any) -> str:
        return str(input)    
    

runnable1 = RunnableLambda(lambda x: {"foo": x})    

configurable_runnable = ListRunnable().configurable_alternatives(
    ConfigurableField(id="second_step"), default_key="list", string=StrRunnable()
)
chain = runnable1 | configurable_runnable


### 1. 'second_step'을 'string'로 설정
print(chain.invoke(7, config={"configurable": {"second_step": "string"}}))
# {'foo': 7}

### 2. 'second_step'을 설정하지 않으면 기본값인 'list'로 설정
print('-' * 50)
print(chain.invoke(7))
# [{'foo': 7}]

