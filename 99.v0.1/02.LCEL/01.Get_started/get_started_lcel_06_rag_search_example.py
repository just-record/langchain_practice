# RAG Search Example

# Requires:
# pip install langchain docarray tiktoken

from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings

# 이 경고는 pydantic.error_wrappers:ValidationError이 pydantic:ValidationError으로 이동되었다는 것을 알리는 것입니다1. 이 경고는 코드가 여전히 이전 위치를 참조하고 있기 때문에 발생합니다. 이 경고는 코드가 정상적으로 작동하지만, Pydantic의 향후 버전에서는 ImportError를 발생시킬 수 있습니다1.
# 따라서, 코드에서 pydantic.error_wrappers:ValidationError 대신 pydantic:ValidationError을 사용하도록 수정하는 것이 좋습니다1. 이렇게 하면 경고가 사라지고 코드가 향후 Pydantic 버전과 호환될 것입니다1. 만약 ValidationError를 직접 가져오지 않았다면, 사용 중인 라이브러리 중 하나가 그렇게 하고 있을 수 있습니다1.

vectorstore = DocArrayInMemorySearch.from_texts(
    ["harrison worked at kensho", "bears like to eat honey"],
    embedding=OpenAIEmbeddings(),
)

# print(f'Vectorstore s type: {type(vectorstore)}')

retriever = vectorstore.as_retriever()

template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI()
output_parser = StrOutputParser()

setup_and_retrieval = RunnableParallel(
    {"context": retriever, "question": RunnablePassthrough()}
)

# print(f'RunnableParallel type: {type(setup_and_retrieval)}')
# print(f'RunnableParallel: {setup_and_retrieval}')

# chain = setup_and_retrieval | prompt | model | output_parser
# Error
# pydantic_core._pydantic_core.ValidationError: 2 validation errors for DocArrayDoc
# text
#   Field required [type=missing, input_value={'embedding': [-0.0192381..., 0.010137099064823456]}, input_type=dict]
#     For further information visit https://errors.pydantic.dev/2.6/v/missing
# metadata
#   Field required [type=missing, input_value={'embedding': [-0.0192381..., 0.010137099064823456]}, input_type=dict]
#     For further information visit https://errors.pydantic.dev/2.6/v/missing

# 아마 버전 문제일 것 같은데 지금은 잘 모르겠다.

# 1
# chain = setup_and_retrieval
# 위와 동일 에러

# 2
# chain = prompt | model | output_parser
# print(chain.invoke({'context': retriever, 'question': "where did harrison work?"}))

# 우선 출력은 되는데 맞는지 모르겠다. 문장에 어디서 일하는지 정보가 있는지 없다고 나온다.
# Based on the given context, there is no information available about where Harrison worked.

# 3 - 조금 더 고쳐 봄
# chain = prompt | model | output_parser
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains import create_retrieval_chain
# document_chain = create_stuff_documents_chain(model, prompt)
# retrieval_chain = create_retrieval_chain(retriever, document_chain)
# print(retrieval_chain.invoke({'context': retriever, 'question': "where did harrison work?"}))

# KeyError: 'input'

# 4 - 3을 조금 더 수정 해 봄
chain = prompt | model | output_parser
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
document_chain = create_stuff_documents_chain(model, prompt)
retrieval_chain = create_retrieval_chain(retriever, document_chain)
print(retrieval_chain.invoke({'context': retriever, 'input': "where did harrison work?"}))

# 처음과 동일한 에러
# pydantic_core._pydantic_core.ValidationError: 2 validation errors for DocArrayDoc
# text
#   Field required [type=missing, input_value={'embedding': [-0.0192381..., 0.010137099064823456]}, input_type=dict]
#     For further information visit https://errors.pydantic.dev/2.6/v/missing
# metadata
#   Field required [type=missing, input_value={'embedding': [-0.0192381..., 0.010137099064823456]}, input_type=dict]
#     For further information visit https://errors.pydantic.dev/2.6/v/missing