from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

llm = ChatOpenAI()
# llm = ChatOpenAI(openai_api_key="...")

result = llm.invoke("how can langsmith help with testing?")
print(result)



