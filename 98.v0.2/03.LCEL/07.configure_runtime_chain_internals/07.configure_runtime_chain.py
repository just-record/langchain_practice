
from dotenv import load_dotenv
load_dotenv()

from langchain_anthropic import ChatAnthropic
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


prompt = PromptTemplate.from_template(
    "Tell me a joke about {topic}"
).configurable_alternatives(
    # This gives this field an id
    # When configuring the end runnable, we can then use this id to configure this field
    ConfigurableField(id="prompt"),
    # This sets a default_key.
    # If we specify this key, the default LLM (ChatAnthropic initialized above) will be used
    default_key="joke",
    # This adds a new option, with name `poem`
    poem = PromptTemplate.from_template("Write a short poem about {topic}"),
    # You can add more configuration options here    
)

chain = prompt | llm

### llm: gpt4o로 chain(gpt4o_joke)를 저장
gpt4o_joke = chain.with_config(configurable={"llm": "gpt4o"})

results = gpt4o_joke.invoke({"topic": "bears"})
print(results)
# 출력: 'model_name': 'gpt-4o-2024-05-13'
# content='Sure, here\'s a bear-related joke for you:\n\nWhy did the bear wear a vest?\n\nBecause he wanted to be a "vest"-ed interest!' response_metadata={'token_usage': {'completion_tokens': 30, 'prompt_tokens': 13, 'total_tokens': 43}, 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_d576307f90', 'finish_reason': 'stop', 'logprobs': None} id='run-520cc254-13f0-43b1-9097-387affce4b53-0' usage_metadata={'input_tokens': 13, 'output_tokens': 30, 'total_tokens': 43}