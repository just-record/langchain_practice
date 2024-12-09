from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda

prompt = ChatPromptTemplate.from_template("tell me a story about {topic}")

model = ChatOpenAI()

# chain_with_coerced_function = prompt | model | RunnableLambda(lambda x: x.content[:5])
chain_with_coerced_function = prompt | model | (lambda x: x.content[:5])

results = chain_with_coerced_function.invoke({"topic": "bears"})
print(results)