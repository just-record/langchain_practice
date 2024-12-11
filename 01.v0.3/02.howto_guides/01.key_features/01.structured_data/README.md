# How-to guides - Key features - How to return structured data from a model

<https://python.langchain.com/docs/how_to/structured_output/>

- conceptual guide: <https://python.langchain.com/docs/concepts/structured_outputs/>

## The `.with_structured_output()` method

**Tool을 calling**

- 위 함수의 기능을 제공하는 모델: <https://python.langchain.com/docs/integrations/chat/>

### Pydantic class

- 01.structured_output_pydantic.py: Pydantic을 사용 하여 구조화된 출력을 반환

### TypedDict or JSON Schema

- 02.structured_output_typeddict.py: TypedDict를 사용하여 구조화된 출력을 반환(인자 유효성-X, 스트리밍-O)

### Choosing between multiple schemas

- 03.choosing_multiple_schema.py: 다중 schema 중 인공지능이 선택하여 사용

### Streaming

- 04.streaming.py

### Few-shot prompting

- 05.few_shot_prompting.py

### (Advanced) Speccifying the method for structuring outputs

- 06.specifying_method.py: json mode

### (Advanced) Raw output

- 07.raw_output.py: include_raw=True 로 raw output을 반환

## Prompting and parsing model outputs directly

## Using `PydanticOutputParser`

**OutputParser를 통해 Prompt를 생성**

- 08.pydantic_output_parser.py: 내장되어 있음

## Custom Parsing

- 09.custom_parsing.py: 우선 소스 코드 작성 - 최종적으로 분석 하지 않음. 필요 할 때 보면 될 듯