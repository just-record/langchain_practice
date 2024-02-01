# Model

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template("tell me a short joke about {topic}")
prompt_value = prompt.invoke({"topic": "ice cream"})
model = ChatOpenAI(model="gpt-4")
message = model.invoke(prompt_value)

print(type(message))
# <class 'langchain_core.messages.ai.AIMessage'>

print(message)
# content="Why don't ice creams ever get invited to parties?\n\nBecause they always melt under pressure!"