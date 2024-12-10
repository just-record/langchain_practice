# pip install -qU langchain-community
from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

file_path = "./nke-10k-2023.pdf"
loader = PyPDFLoader(file_path)

docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

##################################################################################
from langchain_community.vectorstores import FAISS

##################################################################################
### 1. vector store 생성
print('1.', '-' * 50)
##################################################################################
# vector_store = InMemoryVectorStore(embeddings)
# vector_store = Chroma(embedding_function=embeddings)
vector_store = FAISS(embedding_function=embeddings)
rprint(vector_store)
### 오류 발생 ###
# 1. --------------------------------------------------
# Traceback (most recent call last):
#     vector_store = FAISS(embedding_function=embeddings)
# TypeError: FAISS.__init__() missing 3 required positional arguments: 'index', 'docstore', and 'index_to_docstore_id'



##################################################################################
### 2. vector store에 Embedding된 vector 추가
print('2.', '-' * 50)
##################################################################################
ids = vector_store.add_documents(documents=all_splits)
rprint(ids[:3])


##################################################################################
### 3. similarity search
print('3.', '-' * 50)
##################################################################################
results = vector_store.similarity_search(
    "How many distribution centers does Nike have in the US?"
)

print(results[0])
print(' ')
rprint(results)


##################################################################################
### 4. 비동기 검색
print('4.', '-' * 50)
##################################################################################
import asyncio

async def search_nike():
    results = await vector_store.asimilarity_search("When was Nike incorporated?")
    return results[0]

results = asyncio.run(search_nike())
print(results)


##################################################################################
### 5. 점수를 포함 검색
print('5.', '-' * 50)
##################################################################################
# Note that providers implement different scores; the score here
# is a distance metric that varies inversely with similarity.

results = vector_store.similarity_search_with_score("What was Nike's revenue in 2023?")
doc, score = results[0]
print(f"Score: {score}\n")
rprint(doc)


##################################################################################
### 6. 임베딩 된 vector로 검색
print('6.', '-' * 50)
##################################################################################
embedding = embeddings.embed_query("How were Nike's margins impacted in 2023?")

results = vector_store.similarity_search_by_vector(embedding)
rprint(results[0])
