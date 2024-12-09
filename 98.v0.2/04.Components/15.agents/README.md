# Agents

<https://python.langchain.com/v0.2/docs/how_to/#agents>

For in depth how-to guides for agents, please check out LangGraph documentation
- <https://langchain-ai.github.io/langgraph/>

추후에 langgraph에 대해 알아봐야 겠다.

## How to

### Build an Agent with AgentExecutor (Legacy)

<https://python.langchain.com/v0.2/docs/how_to/agent_executor/>

#### LangSmith

LangChain의 추적 로깅 서비스

<https://smith.langchain.com/>

- LangSmith 가입
  - <https://docs.smith.langchain.com/>
  - 참조사이트: <https://blog.mesmerist.net/entry/langsmith-%EC%84%A4%EC%A0%95%ED%95%98%EA%B8%B0>
- `.env` 파일에 환경변수 설정 추가 하기

```text
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=<발급받은 API key>
LANGCHAIN_PROJECT=<원하는 프로젝트 명> # 예: LANGCHAIN_PRACTICE
```

- 01.langsmith_quickstart.py: langsmith 사용 예시
  - LangSmith 사이트 로그인
  - 'Projects' -> 'LANGCHAIN_PRACTICE' -> 'pipeline' -> TRACE 확인
    - 'pipeline': Input - 'user_input: Hello, world!', Output - 'Hello! How may I assist you today?'
    - 'ChatOpenAI', 'gpt-3.5-turbo': Input - 'Hello, world!', Output - 'Hello! How may I assist you today?'

#### Agent

- 'Tavily' tool을 사용 하기 위해 API-Key 발급 받기: <https://app.tavily.com/sign-in>
- `.env` 파일에 환경변수 설정 추가 하기

```text
TAVILY_API_KEY=<발급받은 API key>
```

- 02.creage_and_run_agent.py: 'tools'을 정의 하고 모델에 바인딩하고 agent는 생성 하고 agent를 실행 하는 예시
- 03.add_memory_agent.py: agent에 이전 대화를 기억하도록 하는 예시

> 결론

- [How to use LangGraph's built-in versions of AgentExecutor](https://python.langchain.com/v0.2/docs/how_to/migrate_agent/)
- [How to create a custom agent](https://python.langchain.com/v0.1/docs/modules/agents/how_to/custom_agent/)
- [How to stream responses from an agent](https://python.langchain.com/v0.1/docs/modules/agents/how_to/streaming/)
- [How to return structured output from an agent](https://python.langchain.com/v0.1/docs/modules/agents/how_to/agent_structured/)

### How to migrate from legacy LangChain agents to LangGraph

<https://python.langchain.com/v0.2/docs/how_to/migrate_agent/>

- 04.migrate_agent_to_langgraph_basicusage.py: 'langgraph'를 사용하여 agent를 생성하고 실행 하는 기본 예시
- 05.migrate_agent_to_langgraph_prompt.py: 'langgraph'를 사용하여 prompt없이 agent를 생성하고 실행 하는 예시
- 06.migrate_agent_to_langgraph_memory.py: 'langgraph'를 사용하여 이전 대화를 기억하도록 하는 예시
- 07.migrate_agent_to_langgraph_iterating.py: 'langgraph'를 사용하여 단계를 반복 하는 예시
- 08.return_intermediate_steps.py: 'langgraph'를 사용하여 단계별 결과를 반환 하는 예시
- 09.max_iterations.py: 'langgraph'를 사용하여 최대 반복 횟수를 설정 하는 예시
- 10.max_execution_time.py: 'langgraph'를 사용하여 최대 실행 시간을 설정 하는 예시 => 잘 안됨
- 11.early_stopping_method.py: 'langgraph'를 사용하여 조기 중지 방법을 설정 하는 예시
- 12.trim_intermediate_steps.py: 'langgraph'를 사용하여 중간 단계를 제거 하는 예시 => 잘 이해가 안됨

LangGraph는 시간을 조금 두고 제대로 분석해봐야 겠다.