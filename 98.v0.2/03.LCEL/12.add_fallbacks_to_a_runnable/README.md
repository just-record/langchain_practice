# add fallbacks to a runnable

<https://python.langchain.com/v0.2/docs/how_to/fallbacks/>

fallbacks: 비상시(API의 문제 발생 - rate limiting, downtime)에 사용 할 수 있는 대안. LLM level 뿐만 아니라 전체 Runnable level에서 적용 가능

- 01.add_fallbacks.py: OpenAI의 gpt-fake(없는 모델)에 error 발생 시 gpt-3.5-turbo로 전환
  - 공식 예제에서는 OpenAI에서 오류가 발생 하면 ChatAnthropic으로 전환
- 02.add_fallbacks.py: 보통의 chain에 fallbacks을 적용
- 03.add_fallbacks.py: Sequences에 fallbacks을 적용 - 다른 모델이 적용 됨에 따른 다른 prompt 적용 하기
- 04.add_fallbacks.py: 긴 입력에 fallbacks을 적용
  - 공식 예제 코드로 재현이 어려워 다은 방식으로 긴 입력 값 생성하고 모델도 gpt-3.5-turbo와 gpt-4o로 변경
- 05.add_fallbacks.py: 빠른고 싼 모델에서 실패하면 더 좋은 모델 사용
  - gpt-3.5-turbo도 성능이 좋아 져서 오류가 발생하지 않음

## 추가 분석

- OpenAI
- PromptTemplate
- DatetimeOutputParser
 