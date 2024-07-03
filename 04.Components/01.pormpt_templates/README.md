# Prompt templates

<https://python.langchain.com/v0.2/docs/how_to/#prompt-templates>

## Prompt templates

<https://python.langchain.com/v0.2/docs/concepts/#prompt-templates>

- 01.string_PromptTemplates.py: 단일 문자열을 포맷팅하여 prompt 생성하기 - 변수 포함
- 02.chat_prompt_templates.py: 메시지 목록을 포맷팅하여 prompt 생성하기 - 'system', 'user', 'ai' - 변수 포함 
- 03.messages_placeholder.py: 특정한 위치에 메시지 목록을 삽입하기

## How to

### How to use few shot examples

<https://python.langchain.com/v0.2/docs/how_to/few_shot_examples/#create-a-formatter-for-the-few-shot-examples>

- 04.example_set.py: few-shot - example-set에서 하나 선택 하기 - FewShotPromptTemplate 사용 하기
- 05.example_selector.py: 'SemanticSimilarityExampleSelector' - embedding vertor를 사용하여 가장 유사한 example 선택 하기 - FewShotPromptTemplate에 최종 적용 하기

### How to use few shot examples in chat models

<https://python.langchain.com/v0.2/docs/how_to/few_shot_examples_chat/>

- 06.fixed_examples.py: 'ChatPromptTemplate', 'FewShotChatMessagePromptTemplate' - 고정 된 examples에 사용
- 07.dynamic_examples.py: 'SemanticSimilarityExampleSelector' - embedding vertor를 사용하여 가장 유사한 example 선택 하기

### How to partially format prompt templates

<https://python.langchain.com/v0.2/docs/how_to/prompts_partial/>

- 08.partial_with_strings.py: 'prompt.partial' 또는 'partial_variables' - prompt의 일부(문자)를 포맷팅 하기
- 09.09.partial_with_function.py: 'prompt.partial' 또는 'partial_variables' - prompt의 일부(함수)를 포맷팅 하기

### How to compose prompts together

- 10.compose_prompts_together.py: 'PipelinePromptTemplate' - 여러 단계의 프롬프트 생성 과정을 하나의 파이프라인으로 연결
