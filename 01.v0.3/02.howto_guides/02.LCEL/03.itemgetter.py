from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from operator import itemgetter
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

vectorstore = FAISS.from_texts(
    ["harrison worked at kensho"], embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever()

template = """Answer the question based only on the following context:
{context}

Question: {question}

Answer in the following language: {language}
"""

# The prompt expects input with keys for "context" and "question"
prompt = ChatPromptTemplate.from_template(template)

model = ChatOpenAI()

chain = (
    {
        "context": itemgetter("question") | retriever,
        "question": itemgetter("question"),
        "language": itemgetter("language"),
    }
    | prompt
    | model
    | StrOutputParser()
)
##################################################################################
### 0. itemgetter란?
### itemgetter는 시퀀스(리스트, 튜플)나 매핑(딕셔너리) 타입의 데이터에서 특정 인덱스나 키의 값을 추출하는 callable 객체를 생성하는 함수
# user = {'name': 'John', 'age': 30}
# get_name = itemgetter('name')
# print(get_name(user))  # 출력: 'John'
print('0.', '-' * 50)
##################################################################################
question_getter = itemgetter("question")
rprint(question_getter({"question": "where did harrison work?"}))


##################################################################################
### 1. 'question'와 language' key를 가져야 함
print('1.', '-' * 50)
##################################################################################
results = chain.invoke({"question": "where did harrison work", "language": "italian"})
rprint(results)
# 1. --------------------------------------------------
# Harrison worked at Kensho.

