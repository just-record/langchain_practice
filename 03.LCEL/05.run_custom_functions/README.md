# run custom functions

<https://python.langchain.com/v0.2/docs/how_to/functions/>

- 01.run_custom_functions.py: 임의의 함수를 'RunnableLambda'의 생성자에 전달하여 Runnable을 만들기
- 02.run_custom_functions.py: '@chain' 데코레이터를 사용하여 임의의 함수를 chain으로 만들기
- 03.run_custom_functions.py: '|' 연산자에 의해 'RunnableLambda' 생략
- 04.run_custom_functions.py: Runnable lambdas는 선택적으로 RunnableConfig 허용 가능 => 잘 이해가 안 감
- 05.run_custom_functions.py: Streamimg - 사용자 정의 출력 파서 => 흐름은 이해 되나 설명이 잘 이해가 안 감
- 06.run_custom_functions.py: Streamimg - 다음 쉼표 생성 하는 사용자 지정 함수 정의 => 흐름은 이해 되나 설명이 잘 이해가 안 감
- 07.run_custom_functions.py: Streamimg - 비동기 버전 (Iterator -> AsyncIterator)

## 추가 분석

- RunnableConfig: <https://api.python.langchain.com/en/latest/runnables/langchain_core.runnables.config.RunnableConfig.html>
- get_openai_callback: <https://api.python.langchain.com/en/latest/callbacks/langchain_community.callbacks.manager.get_openai_callback.html>
