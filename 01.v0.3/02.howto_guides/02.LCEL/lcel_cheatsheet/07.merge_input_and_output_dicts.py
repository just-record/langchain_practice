from langchain_core.runnables import RunnableLambda, RunnablePassthrough

runnable1 = RunnableLambda(lambda x: x["foo"] + 7)

##################################################################################
### 1. 입력과 출력을 병합하기
### assign: 입력 데이터를 그대로 유지하면서 새로운 키-값 쌍을 추가하는 메서드
### {'bar': runnable1}을 추가함
print('1.', '-' * 50)
##################################################################################
chain = RunnablePassthrough.assign(bar=runnable1)

print(chain.invoke({"foo": 10}))
# 1. --------------------------------------------------
# {'foo': 10, 'bar': 17}

### 1. 입력값 {"foo": 10}
### 2. runnable1이 실행되어 {"foo": 10}의 "foo" 키의 값인 10에 7을 더한 17을 반환
### 3. 입력값에 "bar": 17을 추가하여 반환


##################################################################################
### 2. assign 추가 테스트
### 여러 개의 새로운 필드를 순차적으로 추가
print('2.', '-' * 50)
##################################################################################
runnable2 = RunnableLambda(lambda x: x["foo"] * 2)
chain2 = RunnablePassthrough.assign(bar=runnable1).assign(baz=runnable2)
print(chain2.invoke({"foo": 10}))
# 2. --------------------------------------------------
# {'foo': 10, 'bar': 17, 'baz': 20}

### 1. 입력값: {"foo": 10}
### 2. runnable1 실행: bar = 10 + 7 = 17
### 3. runnable2 실행: baz = 10 * 2 = 20
### 4. 최종 출력: {"foo": 10, "bar": 17, "baz": 20}