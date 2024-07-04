# Example selectors

<https://python.langchain.com/v0.2/docs/how_to/#example-selectors>

## Example Selectors

<https://python.langchain.com/v0.2/docs/concepts/#example-selectors>

## How to

### How to use example selectors

<https://python.langchain.com/v0.2/docs/how_to/example_selectors/>

- 01.custom_example_selector.py: 사용자 정의 example selector 만들기

### How to select examples by length

<https://python.langchain.com/v0.2/docs/how_to/example_selectors_length_based/>

- 02.select_examples_by_length.py: 'LengthBasedExampleSelector' - example의 길이에 따라 선택하기

### How to select examples by similarity

<https://python.langchain.com/v0.2/docs/how_to/example_selectors_similarity/>

- 03.select_examples_by_similarity.py: 'SemanticSimilarityExampleSelector' - embedding vertor를 사용하여 가장 유사한 example 선택 하기

### How to select examples by n-gram overlap

<https://python.langchain.com/v0.2/docs/how_to/example_selectors_ngram/>

- 04.select_examples_by_ngram.py: 'NGramOverlapExampleSelector' - n-gram overlap을 사용하여 가장 유사한 example 선택 하기


#### N-gram

- 텍스트를 N개의 연속된 단어나 문자 단위로 쪼개는 것
  - 예: "hello world" - 2-gram은 ["hello", "world"] 또는 ["he", "el", "ll", "lo", "o "]
- N-gram overlap: N-gram 중복 개수가 가장 많은 N-gram을 선택

### How to select examples by maximal marginal relevance (MMR)

<https://python.langchain.com/v0.2/docs/how_to/example_selectors_mmr/>

- 05.select_examples_by_mmr.py: 'MaxMarginalRelevanceExampleSelector',  'SemanticSimilarityExampleSelector' - MMR을 사용하여 가장 유사한 example 선택 하기

#### Maximal marginal relevance (MMR)

- MMR은 정보 검색과 텍스트 요약에서 사용되는 기법으로, 두 가지 중요한 목표를 동시에 달성
  - 관련성 (Relevance): 검색 쿼리나 주제와 가장 관련 있는 정보를 찾는 것.
  - 다양성 (Diversity): 선택된 정보들 사이의 중복을 최소화하는 것.
- 예: imagine you're making a playlist for a party. You want songs that:
  - 파티 분위기와 잘 맞는 노래들 (관련성)
  - 서로 너무 비슷하지 않은 노래들 (다양성)
- 방식
  - 가장 관련성 높은 항목을 먼저 선택
  - 다음 선택은 관련성은 높지만 이미 선택된 항목들과 너무 비슷하지 않은 항목을 선택

