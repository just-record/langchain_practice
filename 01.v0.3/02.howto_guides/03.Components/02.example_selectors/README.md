# How-to guides - Components - Example selectors

<https://python.langchain.com/docs/how_to/#example-selectors>

✔️ conceptual guide: <https://python.langchain.com/docs/concepts/example_selectors/>

## How to use example selectors

- 01.example_selectors.py

예시 선택기 유형

| 이름 | 설명 |
|------|------|
| Similarity | 입력값과 예시 간의 의미적 유사성을 사용하여 어떤 예시를 선택할지 결정합니다. |
| MMR | 입력값과 예시 간의 최대 한계 관련성(Max Marginal Relevance)을 사용하여 어떤 예시를 선택할지 결정합니다. |
| Length | 특정 길이 내에 얼마나 많은 예시가 들어갈 수 있는지를 기준으로 예시를 선택합니다. |
| Ngram | 입력값과 예시 간의 n그램 중복을 사용하여 어떤 예시를 선택할지 결정합니다. |

## How to select examples by length

- 02.select_examples_by_length.py

## How to select examples by similarity

- 03.select_examples_by_similarity.py

## How to select examples by n-gram overlap

- 04.select_examples_by_ngram_overlap.py

## How to select examples by maximal marginal relevance (MMR)

- 05.select_examples_by_mmr.py

## How to select examples from a LangSmith dataset

- 06.select_examples_from_langsmith.py: 오류 발생 
