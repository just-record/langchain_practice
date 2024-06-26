# Entire Pipeline

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template("tell me a short joke about {topic}")
# prompt_value = prompt.invoke({"topic": "ice cream"})
model = ChatOpenAI(model="gpt-4")
# message = model.invoke(prompt_value)
output_parser = StrOutputParser()

input = {"topic": "ice cream"}
print(prompt.invoke(input))
# messages=[HumanMessage(content='tell me a short joke about ice cream')]

print((prompt | model).invoke(input))
# content="Why don't ice creams ever get invited to parties?\n\nBecause they always melt under pressure!"

print((prompt | model | output_parser).invoke(input))
# Why don't ice creams ever get invited to parties?

# Because they always melt under pressure!

