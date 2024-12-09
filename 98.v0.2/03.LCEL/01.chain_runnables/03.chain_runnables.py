from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = ChatOpenAI(model="gpt-3.5-turbo")
prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")

chain = prompt | model | StrOutputParser()

analysis_prompt = ChatPromptTemplate.from_template("is this a funny joke? {joke}")

### 추가 또는 수정 부분 ###
composed_chain_with_lambda = (chain | (lambda input: {"joke": input}) | analysis_prompt | model | StrOutputParser())

results = composed_chain_with_lambda.invoke({"topic": "bears"})

print(results)