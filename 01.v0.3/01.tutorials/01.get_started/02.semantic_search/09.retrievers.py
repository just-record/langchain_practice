from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

file_path = "./nke-10k-2023.pdf"
loader = PyPDFLoader(file_path)

docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

vector_store = InMemoryVectorStore(embeddings)
vector_store.add_documents(documents=all_splits)

##################################################################################
from typing import List

from langchain_core.documents import Document
from langchain_core.runnables import chain

##################################################################################
### 1. Retriver 생성
print('1.', '-' * 50)
##################################################################################
@chain
def retriever(query: str) -> List[Document]:
    return vector_store.similarity_search(query, k=1)


results = retriever.batch(
    [
        "How many distribution centers does Nike have in the US?",
        "When was Nike incorporated?",
    ],
)

rprint(results)
# [
#     [
#         Document(
#             id='37f6662c-e3ad-4a3a-a39f-b53291d8ee5a',
#             metadata={'source': './nke-10k-2023.pdf', 'page': 26, 'start_index': 804},
#             page_content='operations. We also lease an office complex in Shanghai, China, our headquarters for our Greater China geography, occupied by employees focused on 
# implementing our\nwholesale, NIKE Direct and merchandising strategies in the region, among other functions.\nIn the United States, NIKE has eight significant distribution 
# centers. Five are located in or near Memphis, Tennessee, two of which are owned and three of which are\nleased. Two other distribution centers, one located in Indianapolis, 
# Indiana and one located in Dayton, Tennessee, are leased and operated by third-party logistics\nproviders. One distribution center for Converse is located in Ontario, 
# California, which is leased. NIKE has a number of distribution facilities outside the United States,\nsome of which are leased and operated by third-party logistics providers. 
# The most significant distribution facilities outside the United States are located in Laakdal,'
#         )
#     ],
#     [
#         Document(
#             id='14242849-c020-4c6f-9e68-df1dd2104c9c',
#             metadata={'source': './nke-10k-2023.pdf', 'page': 3, 'start_index': 0},
#             page_content='Table of Contents\nPART I\nITEM 1. BUSINESS\nGENERAL\nNIKE, Inc. was incorporated in 1967 under the laws of the State of Oregon. As used in this 
# Annual Report on Form 10-K (this "Annual Report"), the terms "we," "us," "our,"\n"NIKE" and the "Company" refer to NIKE, Inc. and its predecessors, subsidiaries and affiliates,
# collectively, unless the context indicates otherwise.\nOur principal business activity is the design, development and worldwide marketing and selling of athletic footwear, 
# apparel, equipment, accessories and services. NIKE is\nthe largest seller of athletic footwear and apparel in the world. We sell our products through NIKE Direct operations, 
# which are comprised of both NIKE-owned retail stores\nand sales through our digital platforms (also referred to as "NIKE Brand Digital"), to retail accounts and to a mix of 
# independent distributors, licensees and sales'
#         )
#     ]
# ]


##################################################################################
### 2. vector_store의 as_retriver 사용
print('2.', '-' * 50)
##################################################################################
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 1},
)

results = retriever.batch(
    [
        "How many distribution centers does Nike have in the US?",
        "When was Nike incorporated?",
    ],
)

rprint(results)
# 2. --------------------------------------------------
# [
#     [
#         Document(
#             id='6503a6c3-e3a2-406e-b72c-6e591aa5eb0a',
#             metadata={'source': './nke-10k-2023.pdf', 'page': 26, 'start_index': 804},
#             page_content='operations. We also lease an office complex in Shanghai, China, our headquarters for our Greater China geography, occupied by employees focused on 
# implementing our\nwholesale, NIKE Direct and merchandising strategies in the region, among other functions.\nIn the United States, NIKE has eight significant distribution 
# centers. Five are located in or near Memphis, Tennessee, two of which are owned and three of which are\nleased. Two other distribution centers, one located in Indianapolis, 
# Indiana and one located in Dayton, Tennessee, are leased and operated by third-party logistics\nproviders. One distribution center for Converse is located in Ontario, 
# California, which is leased. NIKE has a number of distribution facilities outside the United States,\nsome of which are leased and operated by third-party logistics providers. 
# The most significant distribution facilities outside the United States are located in Laakdal,'
#         )
#     ],
#     [
#         Document(
#             id='711d7494-1cf4-434a-be55-293d59bb2076',
#             metadata={'source': './nke-10k-2023.pdf', 'page': 3, 'start_index': 0},
#             page_content='Table of Contents\nPART I\nITEM 1. BUSINESS\nGENERAL\nNIKE, Inc. was incorporated in 1967 under the laws of the State of Oregon. As used in this 
# Annual Report on Form 10-K (this "Annual Report"), the terms "we," "us," "our,"\n"NIKE" and the "Company" refer to NIKE, Inc. and its predecessors, subsidiaries and affiliates,
# collectively, unless the context indicates otherwise.\nOur principal business activity is the design, development and worldwide marketing and selling of athletic footwear, 
# apparel, equipment, accessories and services. NIKE is\nthe largest seller of athletic footwear and apparel in the world. We sell our products through NIKE Direct operations, 
# which are comprised of both NIKE-owned retail stores\nand sales through our digital platforms (also referred to as "NIKE Brand Digital"), to retail accounts and to a mix of 
# independent distributors, licensees and sales'
#         )
#     ]
# ]