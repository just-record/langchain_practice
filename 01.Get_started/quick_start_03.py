# StrOutputParser

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI()
# llm = ChatOpenAI(openai_api_key="...")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are world class technical documentation writer"),
    ("user", "{input}")
])

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

result = chain.invoke({"input": "how can langsmith help with testing?"})
print(result)