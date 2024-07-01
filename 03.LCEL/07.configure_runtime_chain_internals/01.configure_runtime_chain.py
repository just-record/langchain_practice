
from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI

model = ChatOpenAI(temperature=0).configurable_fields(
    temperature=ConfigurableField(
        id="llm_temperature",  ### (1) id
        name="LLM Temperature",
        description="The temperature of the LLM",
    )
)

### 1. 일반적인 사용법

results = model.invoke("pick a random number")
print(results)
# 출력
# content='27' response_metadata={'token_usage': {'completion_tokens': 1, 'prompt_tokens': 11, 'total_tokens': 12}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-84193f28-431f-4fe3-be00-d0a6c01ab8a0-0' usage_metadata={'input_tokens': 11, 'output_tokens': 1, 'total_tokens': 12}

### 2. ConfigurableField를 사용하여 온도를 조정
# (1)의 id와 동일한 "llm_temperature"를 사용
results = model.with_config(configurable={"llm_temperature": 0.9}).invoke("pick a random number")
print(results)
# 출력
# content='7' response_metadata={'token_usage': {'completion_tokens': 1, 'prompt_tokens': 11, 'total_tokens': 12}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-90ae2617-76d1-4a56-a10f-9e74889587a7-0' usage_metadata={'input_tokens': 11, 'output_tokens': 1, 'total_tokens': 12}