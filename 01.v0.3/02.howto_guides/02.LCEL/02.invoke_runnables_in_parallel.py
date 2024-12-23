from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

vectorstore = FAISS.from_texts(
    ["harrison worked at kensho"], embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever()

##################################################################################
### 0. retriever이 어떻게 작동하지?
print('0.', '-' * 50)
##################################################################################
results = retriever.invoke("where did harrison work?")
rprint(results)
# 0. --------------------------------------------------
# [Document(metadata={}, page_content='harrison worked at kensho')]


template = """Answer the question based only on the following context:
{context}

Question: {question}
"""

# The prompt expects input with keys for "context" and "question"
prompt = ChatPromptTemplate.from_template(template)

model = ChatOpenAI()

##################################################################################
### 1. prompt 입력이 'context'와 question' 2개의 key를 가져야 함
print('1.', '-' * 50)
##################################################################################

retrieval_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

results = retrieval_chain.invoke("where did harrison work?")
rprint(results)
# 1. --------------------------------------------------
# Harrison worked at Kensho.


##################################################################################
### 2. RunnableParallel 사용
print('2.', '-' * 50)
##################################################################################
from langchain_core.runnables import RunnableParallel

retrieval_chain = (
    # RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
    RunnableParallel(context=retriever, question=RunnablePassthrough())
    | prompt
    | model
    | StrOutputParser()
)

results = retrieval_chain.invoke("where did harrison work?")
rprint(results)
# 2. --------------------------------------------------
# Harrison worked at Kensho.