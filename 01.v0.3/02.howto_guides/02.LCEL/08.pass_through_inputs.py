from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint


from langchain_core.runnables import RunnableParallel, RunnablePassthrough

##################################################################################
### 1. RunnablePassthrough(): 이전 단계의 데이터를 변경하지 않고 나중 단계의 입력으로 사용
print('1.', '-' * 50)
##################################################################################

runnable = RunnableParallel(
    passed=RunnablePassthrough(),
    modified=lambda x: x["num"] + 1,
)

results = runnable.invoke({"num": 1})
rprint(results)
# {'passed': {'num': 1}, 'modified': 2}


##################################################################################
### 2. Retrieval Example - 실 사용에 가까운 예제
print('2.', '-' * 50)
##################################################################################
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
"""
prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI()

retrieval_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

results = retrieval_chain.invoke("where did harrison work?")
rprint(results)
# 2. --------------------------------------------------
# Harrison worked at Kensho.

##################################################################################
### 3. RunnablePassthrough().invoke() 사용
print('3.', '-' * 50)
##################################################################################
print(RunnablePassthrough().invoke({"num": 1}))
print(RunnablePassthrough().invoke("where did harrison work?"))
# 3. --------------------------------------------------
# {'num': 1}
# where did harrison work?