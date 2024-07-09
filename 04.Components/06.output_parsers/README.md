# Output parsers

<https://python.langchain.com/v0.2/docs/how_to/#output-parsers>

## Output Parsers

<https://python.langchain.com/v0.2/docs/concepts/#output-parsers>

점점 더 많은 모델들이 이를 자동으로 처리하는 함수(또는 도구) 호출을 지원하고 있어 출력 파싱보다는 함수/도구 호출을 사용하는 것이 권장됩니다.

## How to

### How to use output parsers to parse an LLM response into structured format

<https://python.langchain.com/v0.2/docs/how_to/output_parser_structured/>

- 01.pydantic_output_parser.py: 'PydanticOutputParser', 'SimpleJsonOutputParser' 사용

### How to parse JSON output

<https://python.langchain.com/v0.2/docs/how_to/output_parser_json/>

- 02.json_output_parser.py: 'JsonOutputParser' - 'Pydantic' 사용/미사용 - streaming 가능


### How to parse XML output

<https://python.langchain.com/v0.2/docs/how_to/output_parser_xml/>

- 03.xml_output_parser.py: 'XmlOutputParser'

### How to parse YAML output

<https://python.langchain.com/v0.2/docs/how_to/output_parser_yaml/>

- 04.yaml_output_parser.py: 'YamlOutputParser' 사용

### How to retry when a parsing error occurs

<https://python.langchain.com/v0.2/docs/how_to/output_parser_retry/>

- 05.retry_on_error.py: 'RetryOutputParser' - 출력 파싱 오류 시 재시도

### How to use the output-fixing parser

<https://python.langchain.com/v0.2/docs/how_to/output_parser_fixing/>

- 06.output_fixing_parser.py: 'OutputFixingParser' - Error 발생 - 아직 원인은 못 찾음
  - <https://wikidocs.net/233793>에서도 같은 문제가 발생함

### How to create a custom Output Parser

<https://python.langchain.com/v0.2/docs/how_to/output_parser_custom/>

생략 - 필요 시 분석