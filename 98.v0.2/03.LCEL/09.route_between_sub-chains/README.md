# route between sub-chains

<https://python.langchain.com/v0.2/docs/how_to/routing/>

- 01.route_sub-chains.py: 질문을 분류하기(LangChain, Anthropic, Other)
  - 공식 예제는 ChatAnthropic을 사용 했지만 OpenAI로 변경
- 02.route_sub-chains.py: 'custom function'과 'RunnableLambda'를 사용 하여 sub chain 연결하기 (Recommended)
- 03.route_sub-chains.py: 'RunnableBranch'를 사용 하여 sub chain 연결하기 (Legacy)
- 04.route_sub-chains.py: embedding을 사용하여 의미적으로 유사한 prompt의 sub chain 연결하기

## 추가 분석

- RunnableBranch(legacy라서 분석 하지 않아도 될 듯)
- cosine_similarity
