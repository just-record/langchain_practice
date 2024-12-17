import time

from langchain_core.runnables import RunnableLambda
from langchain_core.tracers.schemas import Run


def on_start(run_obj: Run):
    print("start_time:", run_obj.start_time)


def on_end(run_obj: Run):
    print("end_time:", run_obj.end_time)


##################################################################################
### 1. Runnable 객체에 수명 주기(lifecycle) 리스너를 추가하는 방법
### .with_listeners(): 특정 이벤트가 발생할 때 호출되는 콜백 함수를 추가
# on_start - 실행이 시작, on_end - 실행이 종료
print('1.', '-' * 50)
##################################################################################
runnable1 = RunnableLambda(lambda x: time.sleep(x))
chain = runnable1.with_listeners(on_start=on_start, on_end=on_end)
chain.invoke(2)
# 1. --------------------------------------------------
# start_time: 2024-12-17 08:26:06.330530+00:00
# end_time: 2024-12-17 08:26:08.333128+00:00