from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = ChatOpenAI(model="gpt-3.5-turbo")
prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")

chain = prompt | model | StrOutputParser()

### 추가 또는 수정 부분 ###
analysis_prompt = ChatPromptTemplate.from_template("is this a funny joke? {joke}")

# {"joke": chain}은 첫 번째 체인의 출력을 'joke'라는 키로 저장합니다.
# 다른 2개의 요청을 하나의 체인으로 연결합니다.
composed_chain = {"joke": chain} | analysis_prompt | model | StrOutputParser()

results = composed_chain.invoke({"topic": "bears"})

print(results)