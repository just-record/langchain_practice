# Tools

<https://python.langchain.com/v0.2/docs/how_to/#tools>

## Tools

<https://python.langchain.com/v0.2/docs/concepts/#tools>

## How to

### How to create custom tools

<https://python.langchain.com/v0.2/docs/how_to/custom_tools/>

#### @tool decorator

- 01.tool_decorator.py: '@tool' 데코레이터 사용

#### StructuredTool

- 02.structured_tool.py: 'StrurcturedTool.from_function' 사용

#### Subclass BaseTool

이 정도 수준의 tool을 정의할 필요는 현재 없을 듯 -> 이런게 있다 정도만 알고 넘어 갈 것

- 03.subclass_basetool.py: 'BaseTool' 상속하여 사용

#### How to create async tools

- 04.async_tools.py: 도구의 sync 구현만 제공하더라도 여전히 ainvoke 인터페이스를 사용 가능
  - 사용 시 주의 사항: <https://python.langchain.com/v0.2/docs/how_to/custom_tools/#how-to-create-async-tools>\

#### Handling Tool Errors

- 05.tool_exception_handle_tool_error.py: 'ToolException' 발생 -> 'handle_tool_error'로 오류 처리

### How to use built-in tools and toolkits

<https://python.langchain.com/v0.2/docs/how_to/tools_builtin/>

#### Tools

LangChain은 다수의 3rd 파티 도구 컬렉션을 가지고 있습니다. [사용 가능한 tools 목록](https://python.langchain.com/v0.2/docs/integrations/tools/)

- 06.wikipedia_integration.py: 'WikipediaQueryRun' - 위키피디아 검색 결과 반환

#### Customizing Default Tools

- 07.customizing_default_tools.py: 내장된 이름, 설명, 그리고 인자의 JSON 스키마를 수정 가능
  - 인자의 JSON 스키마를 정의할 때, 입력이 함수와 동일하게 유지 - 변경해서는 안 됨. 각 입력에 대한 사용자 정의 설명을 쉽게 정의

#### How to use built-in toolkits

필요 시 분석: [사용 가능한 toolkits 목록](https://python.langchain.com/v0.2/docs/integrations/toolkits/)

```python
# Initialize a toolkit
toolkit = ExampleTookit(...)

# Get list of tools
tools = toolkit.get_tools()
```

### How to use a model to call tools

<https://python.langchain.com/v0.2/docs/how_to/tool_calling/>

한 번 읽어 볼 것

<https://github.com/just-record/langchain_practice/tree/main/04.Components/03.chat_models>에서 이미 연습 함

### How to pass tool outputs to the model

<https://python.langchain.com/v0.2/docs/how_to/tool_results_pass_to_model/>

- 08.tool_results_pass_to_model.py: 진행 과정
  - 사용자 query를 tool이 bindinge된 모델에 요청 - 대화 이력에 추가
  - 모델은 tool 호출에 관한 정보를 반환 - 대화 이력에 추가
  - tool 호출에 대한 정보로 실제 함수를 호출 -> 함수 호출 결과를 반환 - 대화 이력에 추가
  - 지금까지의 모든 대화 이력(실제 함수 호출 결과 포함)을 다시 모델에 요청 -> 최종 결과를 모델이 반환

### How to add ad-hoc tool calling capability to LLMs and Chat Models

도구 호출을 지원하지 않는 모델을 사용 하는 경우 도구를 호출 하는 대안적인 방법

<https://python.langchain.com/v0.2/docs/how_to/tools_prompting/>

![tool_logic](https://python.langchain.com/v0.2/assets/images/tool_chain-3571e7fbc481d648aff93a2630f812ab.svg)

- 09.tools_prompting.py: 도구 호출을 지원하지 않는 모델(local model)에 도구 호출을 추가
  - local model 구축 -> 도구 생성 -> 도구 호출을 생성 하는 프로프트 작성 -> JSON output parser -> 실제 함수 호출 기능 구현 -> chain으로 연결

### How to pass run time values to a tool

<https://python.langchain.com/v0.2/docs/how_to/tool_runtime/>

- 10.pass_runtime_values_tool.py: run time시에 발생 하는 값을 tool에 전달 하기

### How to add a human-in-the-loop for tools

<https://python.langchain.com/v0.2/docs/how_to/tools_human/>

- 11.human_approval_before_invoke_tool.py: tool 호출 전에 인간 승인 추가
  - input() 방식 => 추후 대화 자체에서 처리 하는 방법 필요

### How to handle tool errors

<https://python.langchain.com/v0.2/docs/how_to/tools_error/>

- 12.handle_tool_errors.py: 'Try/except', 'Fallbacks', 'Retry with exception'

### How to force tool calling behavior

<https://python.langchain.com/v0.2/docs/how_to/tool_choice/>

<https://github.com/just-record/langchain_practice/tree/main/04.Components/03.chat_models>에서 이미 연습 함
