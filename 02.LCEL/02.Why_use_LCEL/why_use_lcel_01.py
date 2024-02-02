from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


prompt = ChatPromptTemplate.from_template("Tell me a short joke about {topic}")
model = ChatOpenAI(model="gpt-3.5-turbo")
output_parser = StrOutputParser()

chain = prompt | model | output_parser

# print(chain.invoke({"topic": "ice cream"}))
# "Why don't ice creams ever get invited to parties?\n\nBecause they always drip when things heat up!"