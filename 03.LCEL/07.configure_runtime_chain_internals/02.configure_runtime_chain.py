
from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI

prompt = PromptTemplate.from_template("Pick a random number above {x}")

model = ChatOpenAI(temperature=0).configurable_fields(
    temperature=ConfigurableField(
        id="llm_temperature",  ### (1) id
        name="LLM Temperature",
        description="The temperature of the LLM",
    )
)

chain = prompt | model

### 1. 일반적인 사용법
results = chain.invoke({"x": 10})
print(results)
# 출력
# content='27' response_metadata={'token_usage': {'completion_tokens': 1, 'prompt_tokens': 14, 'total_tokens': 15}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-30c1549b-a159-4cb1-84c9-d0e5f906da90-0' usage_metadata={'input_tokens': 14, 'output_tokens': 1, 'total_tokens': 15}

### 2. ConfigurableField를 사용하여 온도를 조정
results = chain.with_config(configurable={"llm_temperature": 0.9}).invoke({"x": 10})
print(results)
# 출력
# content='47' response_metadata={'token_usage': {'completion_tokens': 1, 'prompt_tokens': 14, 'total_tokens': 15}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-27b57198-dcf9-4a67-962b-0ae730162b7d-0' usage_metadata={'input_tokens': 14, 'output_tokens': 1, 'total_tokens': 15}

