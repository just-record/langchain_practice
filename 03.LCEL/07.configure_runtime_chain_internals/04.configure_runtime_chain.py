
from dotenv import load_dotenv
load_dotenv()

# from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model = "gpt-3.5-turbo",
    temperature=0
).configurable_alternatives(
    # This gives this field an id
    # When configuring the end runnable, we can then use this id to configure this field
    ConfigurableField(id="llm"),
    # This sets a default_key.
    # If we specify this key, the default LLM (ChatAnthropic initialized above) will be used
    default_key="gpt-3.5-turbo",
    # This adds a new option, with name `openai` that is equal to `ChatOpenAI()`
    gpt4=ChatOpenAI(model="gpt-4"),
    # This adds a new option, with name `openai` that is equal to `ChatOpenAI()`
    gpt4o=ChatOpenAI(model="gpt-4o"),
    # You can add more configuration options here    
)

prompt = PromptTemplate.from_template("Tell me a joke about {topic}")
chain = prompt | llm


### 1. By default it will call gpt-3.5-turbo
results = chain.invoke({"topic": "bears"})
print(results)
# 출력: 'model_name': 'gpt-3.5-turbo-0125'
# content="Why did the bear break up with his girlfriend? \n\nBecause he couldn't bear the relationship any longer!" response_metadata={'token_usage': {'completion_tokens': 21, 'prompt_tokens': 13, 'total_tokens': 34}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-ba49b763-c8e8-4733-9f5a-b36a5d030da4-0' usage_metadata={'input_tokens': 13, 'output_tokens': 21, 'total_tokens': 34}
print('-'*30)

### 2. ConfigurableField를 "llm": "gpt4"
results = chain.with_config(configurable={"llm": "gpt4"}).invoke({"topic": "bears"})
print(results)
# 출력: 'model_name': 'gpt-4-0613'
# content="Why don't bears wear shoes? \n\nBecause they'd still have bear feet!" response_metadata={'token_usage': {'completion_tokens': 16, 'prompt_tokens': 13, 'total_tokens': 29}, 'model_name': 'gpt-4-0613', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-c14df20d-968b-4a42-95e0-41402d216554-0' usage_metadata={'input_tokens': 13, 'output_tokens': 16, 'total_tokens': 29}
print('-'*30)

### 3. ConfigurableField를 "llm": "gpt4o"
results = chain.with_config(configurable={"llm": "gpt4o"}).invoke({"topic": "bears"})
print(results)
# 출력: 'model_name': 'gpt-4o-2024-05-13'
# content="Sure, here's a bear-themed joke for you:\n\nWhy did the bear bring a suitcase to the forest?\n\nBecause it wanted to pack its lunch!" response_metadata={'token_usage': {'completion_tokens': 29, 'prompt_tokens': 13, 'total_tokens': 42}, 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_ce0793330f', 'finish_reason': 'stop', 'logprobs': None} id='run-cc0e3ad1-c7ff-4865-8761-97a1af3a21ab-0' usage_metadata={'input_tokens': 13, 'output_tokens': 29, 'total_tokens': 42}