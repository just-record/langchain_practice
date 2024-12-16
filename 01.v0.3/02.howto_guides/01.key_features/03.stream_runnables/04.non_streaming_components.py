from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini")

#################################################################################
### 1. 스트림을 지원 하지 않는 구성요소
### 'Retrievers'는 스트리밍을 지원하지 않음
print('1.', '-' * 50)
##################################################################################
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings

template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

vectorstore = FAISS.from_texts(
    ["harrison worked at kensho", "harrison likes spicy food"],
    embedding=OpenAIEmbeddings(),
)
retriever = vectorstore.as_retriever()

chunks = [chunk for chunk in retriever.stream("where did harrison work?")]
rprint(chunks)
# 1. --------------------------------------------------
# [[Document(metadata={}, page_content='harrison worked at kensho'), Document(metadata={}, page_content='harrison likes spicy food')]]


#################################################################################
### 2. 스트리밍 가능
### 스트리밍을 지원하지 않는 컴포넌트로 구성된 LCEL 체인이라도 스트리밍 가능
print('2.', '-' * 50)
##################################################################################
retrieval_chain = (
    {
        "context": retriever.with_config(run_name="Docs"),
        "question": RunnablePassthrough(),
    }
    | prompt
    | model
    | StrOutputParser()
)

for chunk in retrieval_chain.stream(
    "Where did harrison work? " "Write 3 made up sentences about this place."
):
    print(chunk, end="|", flush=True)
# 2. --------------------------------------------------
# |H|arrison| worked| at| Kens|ho|.| Kens|ho| is| a| vibrant| tech| company| that| specializes| in| data| analytics| and| artificial| intelligence|.| The| office| is| known| for| its| open|-con|cept| layout|,| fostering| collaboration| and| creativity| among| employees|.| Employees| often| enjoy| weekly| team| lunches| featuring| a| variety| of| cuisines|,| reflecting| the| diverse| tastes| of| the| staff|.||    