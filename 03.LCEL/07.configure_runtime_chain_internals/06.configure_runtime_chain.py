
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

### 1. ConfigurableField - "llm": "gpt4o", "prompt": "poem" (llm과 prompt를 모두 대체)
results = chain.with_config(configurable={"llm": "gpt4o", "prompt": "poem"}).invoke({"topic": "bears"})
print(results)
# 출력: 'model_name': 'gpt-4o-2024-05-13', 짧은 시가 출력
# content="In the forest deep and grand,\nWhere the ancient pines still stand,\nRoams a creature, wild and free,\nKeeper of the mystery.\n\nFur like night and eyes so bright,\nSilent guardian of twilight,\nWith strength that moves the river's flow,\nAnd wisdom from the earth below.\n\nIn the glen where shadows play,\nCubs in meadows softly stray,\nLearning paths their elders tread,\nIn a world of green and red.\n\nThrough the seasons, through the years,\nBearing witness to joys and fears,\nBears remind us, strong and true,\nOf the wild within us too." response_metadata={'token_usage': {'completion_tokens': 120, 'prompt_tokens': 13, 'total_tokens': 133}, 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_d576307f90', 'finish_reason': 'stop', 'logprobs': None} id='run-f23fb0aa-ec24-4a4b-bcfc-ab3fbfc3df86-0' usage_metadata={'input_tokens': 13, 'output_tokens': 120, 'total_tokens': 133}
print('-'*30)

### 2. ConfigurableField - "llm": "gpt4o" (llm만 대체)
results = chain.with_config(configurable={"llm": "gpt4o"}).invoke({"topic": "bears"})
print(results)
# 출력: 'model_name': 'gpt-4o-2024-05-13', joke가 출력
# content='Sure! How about this one:\n\nWhy don’t bears wear shoes?\n\nBecause they prefer to go bearfoot! 🐾😄' response_metadata={'token_usage': {'completion_tokens': 27, 'prompt_tokens': 13, 'total_tokens': 40}, 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_d576307f90', 'finish_reason': 'stop', 'logprobs': None} id='run-386f59fa-e6a0-49df-9c59-ad6f14a63645-0' usage_metadata={'input_tokens': 13, 'output_tokens': 27, 'total_tokens': 40}