# LCEL - LangChain Expression Language

<https://python.langchain.com/docs/how_to/#langchain-expression-language-lcel>

✔️ LangChain Expression Language

Conceptual guide: <https://python.langchain.com/docs/concepts/lcel/>

✔️ LCEL cheatsheet

<https://python.langchain.com/docs/how_to/lcel_cheatsheet/>

- lcel_cheatsheet 디렉토리

✔️ Migration guide

<https://python.langchain.com/docs/versions/migrating_chains/>

## How to: chain runnables

- 01.chain_runnables.py

## How to: stream runnables

- <https://github.com/just-record/langchain_practice/tree/main/01.v0.3/02.howto_guides/01.key_features/03.stream_runnables>와 동일

## How to: invoke runnables in parallel

- 02.invoke_runnables_in_parallel.py
- 03.itemgetter.py
- 04.parallelize steps.py

## How to: add default invocation args to runnables

- 05.default_invocation_args.py
- 06.attaching_openai_tools.py

## How to: turn any function into a runnable

- 07.turn_any_function_into_a_runnable.py

## How to: pass through inputs from one chain step to the next

- 08.pass_through_inputs.py

## How to: configure runnable behavior at runtime

- 09.configurable_fields.py
- 10.configurable_alternatives.py

## How to: add message history (memory) to a chain

- v0.2: RunnableWithMessageHistory 사용, 앞으로도 계속 지원
  - <https://python.langchain.com/v0.2/docs/how_to/message_history/>
- v0.3: LangGraph persistence을 활용하는 것을 권장
  - <https://langchain-ai.github.io/langgraph/concepts/persistence/>


갑자기 LagnGraph가...

- 11.example_message_inputs.py
- 12.example_dictionary_inputs.py
- 13.example_message_history.py

## How to: route between sub-chains

- 14.route_between_sub_chains.py

## How to: create a dynamic (self-constructing) chain

- 15.dynamic_chain.py

## How to: inspect runnables

- 16.inspect_runnables.py

## How to: add fallbacks to a runnable

- 17.add_fallbacks.py

## How to: pass runtime secrets to a runnable

- 18.pass_runtime_secrets.py