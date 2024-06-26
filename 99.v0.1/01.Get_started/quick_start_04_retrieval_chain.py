# Retrieval Chain - 1

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document

loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
docs = loader.load()
embeddings = OpenAIEmbeddings()
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = FAISS.from_documents(documents, embeddings)

prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are world class technical documentation writer"),
#     ("user", "{input}")
# ])

llm = ChatOpenAI()

output_parser = StrOutputParser()


document_chain = create_stuff_documents_chain(llm, prompt)

chain = document_chain | output_parser

# Web의 Text가 아닌 Text를 위해 수동으로 작성
result = chain.invoke({
    "input": "how can langsmith help with testing?",
    "context": [Document(page_content="langsmith can let you visualize test results")]
})

print(result)

# result = document_chain.invoke({"input": "how can langsmith help with testing?"})
# print(result)
