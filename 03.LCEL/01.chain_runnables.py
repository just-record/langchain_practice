from dotenv import load_dotenv
load_dotenv()

# OpenAI의 Chat 모델
from langchain_openai import ChatOpenAI
# 채팅 프롬프트 템플릿
from langchain_core.prompts import ChatPromptTemplate
# 모델 출력을 문자열로 파싱
from langchain_core.output_parsers import StrOutputParser

# ChatOpenAI 모델을 초기화합니다.
model = ChatOpenAI(model="gpt-3.5-turbo")

# {topic}은 나중에 주어질 변수
prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")

# runnable한 것을 연결하여 체인을 구성. '|' 연산자로 순차적으로 연결
chain = prompt | model | StrOutputParser()

# 체인을 실행. "bears" -> topic
results = chain.invoke({"topic": "bears"})

print(results)