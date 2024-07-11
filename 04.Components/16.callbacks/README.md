# Callbacks

<https://python.langchain.com/v0.2/docs/how_to/#callbacks>

## Callbacks

<https://python.langchain.com/v0.2/docs/concepts/#callbacks>

Callbacks allow you to hook into the various stages of your LLM application's execution.

## How to

### How to pass callbacks in at runtime

<https://python.langchain.com/v0.2/docs/how_to/callbacks_runtime/>

- 01.pass_callbacks_runtime.py: 'config'로 'callbacks'를 전달

### How to attach callbacks to a runnable

<https://python.langchain.com/v0.2/docs/how_to/callbacks_attach/>

- 02.attach_callbacks_to_runnable.py: '.with_config()'로 'callbacks'를 첨부

### How to propagate callbacks constructor

<https://python.langchain.com/v0.2/docs/how_to/callbacks_constructor/>

생성자 콜백은 그것이 정의된 객체에만 국한되며 객체의 자식들에 의해 상속되지 않습니다.

- 03.propagate_callbacks_constructor.py: module '생성자'로 'callbacks'를 전파

### How to create custom callback handlers

<https://python.langchain.com/v0.2/docs/how_to/custom_callbacks/>

- 04.custom_callback_handlers.py: 사용자 정의 'callbacks' 핸들러 생성

### How to use callbacks in async environments

<https://python.langchain.com/v0.2/docs/how_to/callbacks_async/>

'DNAGER' 읽어 볼 것

- 05.use_callbacks_in_async_environments.py: 'AsyncCallbackHandler'로 비동기 환경에서 'callbacks' 사용