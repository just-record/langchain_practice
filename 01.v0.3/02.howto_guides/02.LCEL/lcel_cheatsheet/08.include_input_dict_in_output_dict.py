from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)

runnable1 = RunnableLambda(lambda x: x["foo"] + 7)

##################################################################################
### 1. 입력 데이터를 출력에 포함하기
### RunnablePassthrough()를 사용하여 입력 데이터를 출력 결과의 일부로 포함
print('1.', '-' * 50)
##################################################################################
chain = RunnableParallel(bar=runnable1, baz=RunnablePassthrough())

print(chain.invoke({"foo": 10}))
# 1. --------------------------------------------------
# {'bar': 17, 'baz': {'foo': 10}}

### 07.merge_input_and_output_dicts.py 와 다른 점을 비교 해 보기 ###
