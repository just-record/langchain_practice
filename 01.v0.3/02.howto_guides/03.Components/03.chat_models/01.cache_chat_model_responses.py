from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

from langchain_core.globals import set_llm_cache


# %%time
import time
from langchain_core.caches import InMemoryCache

set_llm_cache(InMemoryCache())


#################################################################################
### 1. # The first time, it is not yet in cache, so it should take longer
print('1.', '-' * 50)
##################################################################################
start_time = time.time()
rprint(llm.invoke("Tell me a joke").content)
end_time = time.time()
print(f"Execution time: {end_time - start_time:.2f} seconds")
# 1. --------------------------------------------------
# Why did the scarecrow win an award?

# Because he was outstanding in his field!
# Execution time: 0.90 seconds


#################################################################################
### 2. # The second time it is, so it goes faster
print('2.', '-' * 50)
##################################################################################
start_time = time.time()
rprint(llm.invoke("Tell me a joke").content)
end_time = time.time()
print(f"Execution time: {end_time - start_time:.2f} seconds")
# 2. --------------------------------------------------
# Why did the scarecrow win an award?

# Because he was outstanding in his field!
# Execution time: 0.00 seconds


###########################################################
# !rm .langchain.db

# We can do the same thing with a SQLite cache
from langchain_community.cache import SQLiteCache

set_llm_cache(SQLiteCache(database_path=".langchain.db"))

#################################################################################
### 3. SQLite Cache - The first time, it is not yet in cache, so it should take longer
print('3.', '-' * 50)
##################################################################################
start_time = time.time()
rprint(llm.invoke("Tell me a joke").content)
end_time = time.time()
print(f"Execution time: {end_time - start_time:.2f} seconds")
# 3. --------------------------------------------------
# Why don't scientists trust atoms? 

# Because they make up everything!
# Execution time: 0.74 seconds


#################################################################################
### 4. SQLite Cache - The second time it is, so it goes faster
print('4.', '-' * 50)
##################################################################################
start_time = time.time()
rprint(llm.invoke("Tell me a joke").content)
end_time = time.time()
print(f"Execution time: {end_time - start_time:.2f} seconds")
# 4. --------------------------------------------------
# Why don't scientists trust atoms? 

# Because they make up everything!
# Execution time: 0.03 seconds