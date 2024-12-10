# pip install -qU langchain-openai
from rich import print as rprint
from langchain_community.document_loaders import PyPDFLoader

file_path = "./nke-10k-2023.pdf"
loader = PyPDFLoader(file_path)

docs = loader.load()

from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)

##################################################################################
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

##################################################################################
### 1. Embedding model
print('1.', '-' * 50)
##################################################################################
rprint(embeddings)
# OpenAIEmbeddings(
#     client=<openai.resources.embeddings.Embeddings object at 0x7b431abd68f0>,
#     async_client=<openai.resources.embeddings.AsyncEmbeddings object at 0x7b4319d87820>,
#     model='text-embedding-3-large',
#     dimensions=None,
#     deployment='text-embedding-ada-002',
#     openai_api_version=None,
#     openai_api_base=None,
#     openai_api_type=None,
#     openai_proxy=None,
#     embedding_ctx_length=8191,
#     openai_api_key=SecretStr('**********'),
#     openai_organization=None,
#     allowed_special=None,
#     disallowed_special=None,
#     chunk_size=1000,
#     max_retries=2,
#     request_timeout=None,
#     headers=None,
#     tiktoken_enabled=True,
#     tiktoken_model_name=None,
#     show_progress_bar=False,
#     model_kwargs={},
#     skip_empty=False,
#     default_headers=None,
#     default_query=None,
#     retry_min_seconds=4,
#     retry_max_seconds=20,
#     http_client=None,
#     http_async_client=None,
#     check_embedding_ctx_length=True
# )


##################################################################################
### 2. Embedding 하기
print('2.', '-' * 50)
##################################################################################
vector_1 = embeddings.embed_query(all_splits[0].page_content)
vector_2 = embeddings.embed_query(all_splits[1].page_content)

assert len(vector_1) == len(vector_2)
print(f"Generated vectors of length {len(vector_1)}\n")
print(vector_1[:10])
# 2. --------------------------------------------------
# Generated vectors of length 3072
# [0.009310339577496052, -0.016094569116830826, 0.0003302231780253351, 0.006330905947834253, 0.020483998581767082, -0.03916720300912857, -0.007359482813626528, 0.041043028235435486, -0.008028526790440083, 0.05992632359266281]