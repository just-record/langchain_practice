import time

from langchain_core.runnables import RunnableLambda
from langchain_core.tracers.schemas import Run


def on_start(run_obj: Run):
    print("start_time:", run_obj.start_time)


def on_end(run_obj: Run):
    print("end_time:", run_obj.end_time)


runnable1 = RunnableLambda(lambda x: time.sleep(x))
chain = runnable1.with_listeners(on_start=on_start, on_end=on_end)

### 'with_listeners': 실행 시 특정 이벤트가 발생할 때 호출되는 콜백 함수를 추가
# on_start - 실행이 시작, on_end - 실행이 종료

chain.invoke(2)