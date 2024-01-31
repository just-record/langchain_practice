from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI()
# llm = ChatOpenAI(openai_api_key="...")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are world class technical documentation writer"),
    ("user", "{input}")
])

chain = prompt | llm

result = chain.invoke({"input": "how can langsmith help with testing?"})
print(result)



