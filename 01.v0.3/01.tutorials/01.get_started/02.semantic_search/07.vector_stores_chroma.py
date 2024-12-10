# pip install -qU langchain-chroma
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
from langchain_chroma import Chroma

##################################################################################
### 1. vector store 생성
print('1.', '-' * 50)
##################################################################################
# vector_store = InMemoryVectorStore(embeddings)
vector_store = Chroma(embedding_function=embeddings)
rprint(vector_store)
# 1. --------------------------------------------------
# <langchain_chroma.vectorstores.Chroma object at 0x7b7a65238bb0>


##################################################################################
### 2. vector store에 Embedding된 vector 추가
print('2.', '-' * 50)
##################################################################################
ids = vector_store.add_documents(documents=all_splits)
rprint(ids[:3])
# 2. --------------------------------------------------
# ['8278f510-8f74-41ad-96f2-0f6ba9c03dae', '27c66e72-ef15-488e-a177-cfeb1bce50a8', 'd1924fa5-0122-42a7-9513-2cbf004a2e14']


##################################################################################
### 3. similarity search
print('3.', '-' * 50)
##################################################################################
results = vector_store.similarity_search(
    "How many distribution centers does Nike have in the US?"
)

print(results[0])
# 3. --------------------------------------------------
# page_content='operations. We also lease an office complex in Shanghai, China, our headquarters for our Greater China geography, occupied by employees focused on implementing our
# wholesale, NIKE Direct and merchandising strategies in the region, among other functions.
# In the United States, NIKE has eight significant distribution centers. Five are located in or near Memphis, Tennessee, two of which are owned and three of which are
# leased. Two other distribution centers, one located in Indianapolis, Indiana and one located in Dayton, Tennessee, are leased and operated by third-party logistics
# providers. One distribution center for Converse is located in Ontario, California, which is leased. NIKE has a number of distribution facilities outside the United States,
# some of which are leased and operated by third-party logistics providers. The most significant distribution facilities outside the United States are located in Laakdal,' metadata={'page': 26, 'source': './nke-10k-2023.pdf', 'start_index': 804}
print(' ')
rprint(results)
# [
#     Document(
#         metadata={'page': 26, 'source': './nke-10k-2023.pdf', 'start_index': 804},
#         page_content='operations. We also lease an office complex in Shanghai, China, our headquarters for our Greater China geography, occupied by employees focused on 
# implementing our\nwholesale, NIKE Direct and merchandising strategies in the region, among other functions.\nIn the United States, NIKE has eight significant distribution 
# centers. Five are located in or near Memphis, Tennessee, two of which are owned and three of which are\nleased. Two other distribution centers, one located in Indianapolis, 
# Indiana and one located in Dayton, Tennessee, are leased and operated by third-party logistics\nproviders. One distribution center for Converse is located in Ontario, 
# California, which is leased. NIKE has a number of distribution facilities outside the United States,\nsome of which are leased and operated by third-party logistics providers. 
# The most significant distribution facilities outside the United States are located in Laakdal,'
#     ),
#     Document(
#         metadata={'page': 4, 'source': './nke-10k-2023.pdf', 'start_index': 3125},
# ... 생략 ...
# ]


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
# 4. --------------------------------------------------
# page_content='Table of Contents
# PART I
# ITEM 1. BUSINESS
# GENERAL
# NIKE, Inc. was incorporated in 1967 under the laws of the State of Oregon. As used in this Annual Report on Form 10-K (this "Annual Report"), the terms "we," "us," "our,"
# "NIKE" and the "Company" refer to NIKE, Inc. and its predecessors, subsidiaries and affiliates, collectively, unless the context indicates otherwise.
# Our principal business activity is the design, development and worldwide marketing and selling of athletic footwear, apparel, equipment, accessories and services. NIKE is
# the largest seller of athletic footwear and apparel in the world. We sell our products through NIKE Direct operations, which are comprised of both NIKE-owned retail stores
# and sales through our digital platforms (also referred to as "NIKE Brand Digital"), to retail accounts and to a mix of independent distributors, licensees and sales' metadata={'page': 3, 'source': './nke-10k-2023.pdf', 'start_index': 0}


##################################################################################
### 5. 점수를 포함 검색
print('5.', '-' * 50)
##################################################################################
# Note that providers implement different scores; the score here
# is a distance metric that varies inversely with similarity.

results = vector_store.similarity_search_with_score("What was Nike's revenue in 2023?")
doc, score = results[0]
print(f"Score: {score}\n")
# Score: 0.6236849427223206
rprint(doc)
# Document(
#     metadata={'page': 35, 'source': './nke-10k-2023.pdf', 'start_index': 0},
#     page_content='Table of Contents\nFISCAL 2023 NIKE BRAND REVENUE HIGHLIGHTSThe following tables present NIKE Brand revenues disaggregated by reportable operating segment, 
# distribution channel and major product line:\nFISCAL 2023 COMPARED TO FISCAL 2022\n• NIKE, Inc. Revenues were $51.2 billion in fiscal 2023, which increased 10% and 16% compared
# to fiscal 2022 on a reported and currency-neutral basis, respectively.\nThe increase was due to higher revenues in North America, Europe, Middle East & Africa ("EMEA"), APLA 
# and Greater China, which contributed approximately 7, 6,\n2 and 1 percentage points to NIKE, Inc. Revenues, respectively.\n• NIKE Brand revenues, which represented over 90% of 
# NIKE, Inc. Revenues, increased 10% and 16% on a reported and currency-neutral basis, respectively. This\nincrease was primarily due to higher revenues in Men\'s, the Jordan 
# Brand, Women\'s and Kids\' which grew 17%, 35%,11% and 10%, respectively, on a wholesale\nequivalent basis.'
# )


##################################################################################
### 6. 임베딩 된 vector로 검색
print('6.', '-' * 50)
##################################################################################
embedding = embeddings.embed_query("How were Nike's margins impacted in 2023?")

results = vector_store.similarity_search_by_vector(embedding)
rprint(results[0])
# 6. --------------------------------------------------
# Document(
#     metadata={'page': 36, 'source': './nke-10k-2023.pdf', 'start_index': 0},
#     page_content='Table of Contents\nGROSS MARGIN\nFISCAL 2023 COMPARED TO FISCAL 2022\nFor fiscal 2023, our consolidated gross profit increased 4% to $22,292 million compared 
# to $21,479 million for fiscal 2022. Gross margin decreased 250 basis points to\n43.5% for fiscal 2023 compared to 46.0% for fiscal 2022 due to the following:\n*Wholesale 
# equivalent\nThe decrease in gross margin for fiscal 2023 was primarily due to:\n• Higher NIKE Brand product costs, on a wholesale equivalent basis, primarily due to higher 
# input costs and elevated inbound freight and logistics costs as well as\nproduct mix;\n• Lower margin in our NIKE Direct business, driven by higher promotional activity to 
# liquidate inventory in the current period compared to lower promotional activity in\nthe prior period resulting from lower available inventory supply;\n• Unfavorable changes in
# net foreign currency exchange rates, including hedges; and\n• Lower off-price margin, on a wholesale equivalent basis.\nThis was partially offset by:'
# )