# Output parser

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template("tell me a short joke about {topic}")
prompt_value = prompt.invoke({"topic": "ice cream"})
model = ChatOpenAI(model="gpt-4")
message = model.invoke(prompt_value)
output_parser = StrOutputParser()
response = output_parser.invoke(message)

print(type(response))
# <class 'str'>

print(response)
# Why don't ice creams ever get invited to parties?
# 
# Because they always melt under pressure!