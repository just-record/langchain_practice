# add default invocation args to a Runnable

<https://python.langchain.com/v0.2/docs/how_to/binding/>

- 01.add_args.py: model.bind()를 사용하지 않은 기본 예제 코드
- 02.add_args.py: model.bind() 사용 - Runnable 내에서 상수 인수를 포함하여 호출하기 (이전 Runnable의 출력X, 사용자 입력X)
- 03.add_args.py: model.bind(tools=) 사용 하여 OpenAI tools 를 첨부
  - 03.01.add_args.py: tools가 필요 없는 질문. tools에 해당하는 function을 defind 함 => 아직 function을 호출하는 단계는 아님


## 추가 분석

- OpenAI tools