from typing import Any, Optional

from langchain_core.runnables import (
    ConfigurableField,
    RunnableConfig,
    RunnableSerializable,
)

from langchain_core.runnables import RunnableConfig, RunnableLambda, RunnableParallel


class ListRunnable(RunnableSerializable[Any, list]):
    def invoke(
        self, input: Any, config: Optional[RunnableConfig] = None, **kwargs: Any
    ) -> list:
        return self._call_with_config(self.listify, input, config, **kwargs)

    def listify(self, input: Any) -> list:
        return [input]


class StrRunnable(RunnableSerializable[Any, str]):
    def invoke(
        self, input: Any, config: Optional[RunnableConfig] = None, **kwargs: Any
    ) -> list:
        return self._call_with_config(self.strify, input, config, **kwargs)

    def strify(self, input: Any) -> str:
        return str(input)


runnable1 = RunnableLambda(lambda x: {"foo": x})

##################################################################################
### 1. Runnable 객체의 속성을 동적으로 설정
### configurable_alternatives(): 런타임에 다른 Runnable 구현체로 교체할 수 있는 설정 가능

## 1. ConfigurableField(id="second_step")
# 이 설정 가능한 필드를 식별하는 ID를 지정
# 이 ID는 나중에 config 딕셔너리에서 어떤 구현체를 사용할지 지정할 때 사용됨
# 예: {"configurable": {"second_step": "string"}}

## 2. default_key="list"
# 특별한 설정이 없을 때 사용할 기본 구현체를 지정
# 이 경우 ListRunnable이 기본 구현체가 됨
# 설정을 지정하지 않으면 입력값이 리스트로 변환됨

## 3. string=StrRunnable()
# 대체 가능한 구현체를 키-값 쌍으로 지정
# 키 "string"으로 StrRunnable 구현체를 등록
# config에서 "string"을 지정하면 입력값이 문자열로 변환됨

print('1.', '-' * 50)
##################################################################################
configurable_runnable = ListRunnable().configurable_alternatives(
    ConfigurableField(id="second_step"), default_key="list", string=StrRunnable()
)
chain = runnable1 | configurable_runnable

results = chain.invoke(7, config={"configurable": {"second_step": "string"}})
print(type(results))
print(results)
# 1. --------------------------------------------------
# <class 'str'>
# {'foo': 7}


##################################################################################
### 2. config 를 설정하지 않음
print('2.', '-' * 50)
##################################################################################
results = chain.invoke(7)
print(type(results))
print(results)
# 2. --------------------------------------------------
# <class 'list'>
# [{'foo': 7}]
