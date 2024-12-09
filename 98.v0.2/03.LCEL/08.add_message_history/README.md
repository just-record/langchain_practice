# add message history

<https://python.langchain.com/v0.2/docs/how_to/message_history/>

- 00.add_message_history.py: 'RunnableWithMessageHistory'를 사용 하기 위한 기본 구조 - 실제 실행되지 않음(오류 발생) - 다음 단계에서 설명이 나올 듯
- 01.add_message_history.py: 'RunnableWithMessageHistory'의 기본 사용 법 - session_id, get_session_history() 사용
- 02.add_message_history.py: 'input_messages_key', 'history_messages_key'의 사용 예시
  - 입력은 dict형태이며 dict의 key는 여러 개 일 수 있어 입력의 key를 지정
  - 메시지를 로드한 후의 dict의 어느 키에 저장할지를 지정
- 03.add_message_history.py: 'output_messages_key'의 사용 예시  
  - 모델을 사용 하여 하나의 키만 생성 할 때 저장하는 키로 지정
- 04.add_message_history.py: 'input_messages_key'의 특정 사례 - 모든 메시지 입력, 출력을 단위 키로 저장
  - 키가 하나만 존재
- 05.add_message_history.py: Customization - 다 이해 되지 않음.


## 추가 분석

- MessagesPlaceholder
- ConfigurableFieldSpec