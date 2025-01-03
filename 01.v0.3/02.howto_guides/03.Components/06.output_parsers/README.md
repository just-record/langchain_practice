# How-to guides - Components - Messages

<https://python.langchain.com/docs/how_to/#output-parsers>

✔️ conceptual guide: <https://python.langchain.com/docs/concepts/output_parsers/>

## How to parse text from message objects

- 01.parse_text_from_message_objects.py

## How to use output parsers to parse an LLM response into structured format

- 02.parse_llm_response.py

## How to parse JSON output

- 03.parse_json_output.py

## How to parse XML output

- xml는 사용이 거의 없을 것 같아서 우선순위를 낮추고 추후에 연습

## How to parse YAML output

- 04.parse_yaml_output.py

## How to retry when a parsing error occurs

- 05.retry_parsing_error.py

## How to use the output-fixing parser

- 06.output_fixing_parser.py

## How to create a custom Output Parser

- Custom Output Parser를 만드는 방법 2방법
  - 1. LCEL에서 RunnableLambda 또는 RunnableGenerator 사용하기 -- 대부분의 사용 사례에 강력히 권장
  - 2. 출력 파싱을 위한 기본 클래스 중 하나를 상속받기 -- 이것은 어려운 방법
  - 1번을 강력히 권장하고 2번은 어렵다 하여 2번은 생략
- 07.create_custom_output_parser.py  