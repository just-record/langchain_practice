
from dotenv import load_dotenv
load_dotenv()

# from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model = "gpt-3.5-turbo", temperature=0)

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


### 1. By default it will write a joke
results = chain.invoke({"topic": "bears"})
print(results)
# 출력: joke가 출력
# content="Why did the bear break up with his girlfriend? \n\nBecause he couldn't bear the relationship any longer!" response_metadata={'token_usage': {'completion_tokens': 21, 'prompt_tokens': 13, 'total_tokens': 34}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-8fd4c1a2-f801-4599-b0f3-ac27fd731d15-0' usage_metadata={'input_tokens': 13, 'output_tokens': 21, 'total_tokens': 34}
print('-'*30)

### 2. ConfigurableField를 "prompt": "poem"
results = chain.with_config(configurable={"prompt": "poem"}).invoke({"topic": "bears"})
print(results)
# 출력: 짧은 시가 출력
# content="In the forest deep and wild,\nWhere the trees stand tall and proud,\nThere roams a creature fierce and mild,\nThe mighty bear, so strong and loud.\n\nWith fur as dark as midnight's cloak,\nAnd eyes that gleam with ancient wisdom,\nHe moves with grace, his presence spoke,\nIn the silence of the woodland kingdom.\n\nHe hunts for fish in rushing streams,\nAnd berries ripe on bushes low,\nHis strength and power, like a dream,\nIn the mountains where the cold winds blow.\n\nBut do not fear this noble beast,\nFor he is gentle, kind and true,\nA guardian of the forest's peace,\nA symbol of strength, in all he do.\n\nSo let us honor the bear so grand,\nAnd cherish all that he represents,\nFor in his presence, we understand,\nThe beauty of nature, so immense." response_metadata={'token_usage': {'completion_tokens': 168, 'prompt_tokens': 13, 'total_tokens': 181}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-68a7c228-fb3d-4c67-8059-3fb999fca1fb-0' usage_metadata={'input_tokens': 13, 'output_tokens': 168, 'total_tokens': 181}