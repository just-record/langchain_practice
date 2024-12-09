from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
# <!-- ruff: noqa: F821 -->
from langchain.globals import set_llm_cache
from langchain_community.cache import SQLiteCache
import time


llm = ChatOpenAI(model="gpt-3.5-turbo")

set_llm_cache(SQLiteCache(database_path=".langchain.db"))

### The first time, it is not yet in cache, so it should take longer
start_time = time.time()
print(llm.invoke("Tell me a joke"))
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
# content="Why did the scarecrow win an award?...
# Execution time: 0.8657374382019043 seconds


### The second time it is, so it goes faster
print('-'*30)
start_time = time.time()
print(llm.invoke("Tell me a joke"))
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
# content="Why did the scarecrow win an award?...
# Execution time: 0.03108978271484375 seconds