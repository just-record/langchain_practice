from dotenv import load_dotenv
load_dotenv()

from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

vectorstore = FAISS.from_texts(
    ["harrison worked at kensho"], embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever()
template = """Answer the question based only on the following context:
{context}

Question: {question}
"""

# The prompt expects input with keys for "context" and "question"
prompt = ChatPromptTemplate.from_template(template)

model = ChatOpenAI()

### retriever ###
# retriever는 질문과 가장 유사한 문맥을 찾아 반환
# "where did harrison work?" => retriever는 저장된 텍스트에서 가장 관련이 있는 정보를 검색하여 문맥을 반환 => 이 문맥은 프롬프트 템플릿에서 {context} 자리로 전달
# 01.01.invoke_runnables_in_parallel.py에서 test
### RunnablePassthrough ###
# RunnablePassthrough는 입력된 값을 그대로 다음 단계로 전달하는 함수
# 질문("where did harrison work?")을 그대로 프롬프트 템플릿의 {question} 자리로 전달
retrieval_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    ### 또는 아래와 같이 작성 가능
    # RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
    # RunnableParallel(context=retriever, question=RunnablePassthrough())
    | prompt
    | model
    | StrOutputParser()
)

results = retrieval_chain.invoke("where did harrison work?")
print(results)