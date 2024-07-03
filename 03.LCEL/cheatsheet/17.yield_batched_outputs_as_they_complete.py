# from langchain.globals import set_debug
# set_debug(False)

import time

from langchain_core.runnables import RunnableLambda

# time.sleep(x)는 None을 반환 -> or 연산자는 왼쪽 표현식이 False일 때 오른쪽 표현식을 평가
runnable1 = RunnableLambda(lambda x: time.sleep(x) or print(f"slept {x}"))

for idx, result in runnable1.batch_as_completed([5, 1]):
    print(idx, result)

### batch_as_completed: 입력 리스트의 각 요소를 병렬로 처리

### 실행 후 1초 후
# slept 1
# 1 None
### 실행 후 5초 후(1 No3이 출력 되고 5초 후가 아님)
# slept 5
# 0 None

# Async variant:
# async for idx, result in runnable1.abatch_as_completed([5, 1]):
#     print(idx, result)    