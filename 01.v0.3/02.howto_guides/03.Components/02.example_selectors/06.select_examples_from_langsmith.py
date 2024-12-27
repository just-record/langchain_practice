# LangSmith 데이터셋은 유사도 검색을 기본적으로 지원하여 few-shot 예제를 구축하고 쿼리하는 데 훌륭한 도구입니다.

### pip install ###
# pip install -qU "langsmith>=0.1.101" "langchain-core>=0.2.34" langchain langchain-openai langchain-benchmarks

### .env ###
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
# LANGCHAIN_API_KEY=lsv2_...
# LANGCHAIN_PROJECT=LANGCHAIN_PRACTICE

from dotenv import load_dotenv
load_dotenv()

from langsmith import Client as LangSmith

ls_client = LangSmith()

dataset_name = "multiverse-math-few-shot-examples-v2"
dataset_public_url = (
    "https://smith.langchain.com/public/620596ee-570b-4d2b-8c8f-f828adbe5242/d"
)

ls_client.clone_public_dataset(dataset_public_url)

dataset_id = ls_client.read_dataset(dataset_name=dataset_name).id

ls_client.index_dataset(dataset_id=dataset_id)
### 오류 발생 ###
# langsmith.utils.LangSmithError: Failed to POST /datasets/d9709b43-8c86-4191-babb-f11128fcd648/index in LangSmith API. HTTPError('403 Client Error: Forbidden for url: https://api.smith.langchain.com/datasets/d9709b43-8c86-4191-babb-f11128fcd648/index', '{"detail":"Organization does not have permission to index datasets."}')

# examples = ls_client.similar_examples(
#     {"question": "whats the negation of the negation of the negation of 3"},
#     limit=3,
#     dataset_id=dataset_id,
# )
# len(examples)


# examples[0].inputs["question"]
# examples[0].outputs["conversation"]
