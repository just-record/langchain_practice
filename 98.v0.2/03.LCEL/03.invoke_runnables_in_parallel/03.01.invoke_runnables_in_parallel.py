from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_openai import ChatOpenAI
import time

model = ChatOpenAI()
joke_chain = ChatPromptTemplate.from_template("tell me a joke about {topic}") | model
poem_chain = (
    ChatPromptTemplate.from_template("write a 2-line poem about {topic}") | model
)

map_chain = RunnableParallel(joke=joke_chain, poem=poem_chain)


start_time = time.time()
joke_result = joke_chain.invoke({"topic": "bear"})
end_time = time.time()
print(f"Joke Chain Execution Time: {end_time - start_time} seconds")
print(joke_result)


start_time = time.time()
poem_result = poem_chain.invoke({"topic": "bear"})
end_time = time.time()
print(f"Poem Chain Execution Time: {end_time - start_time} seconds")
print(poem_result)


start_time = time.time()
results = map_chain.invoke({"topic": "bear"})
end_time = time.time()
print(f"Parallel Chain Execution Time: {end_time - start_time} seconds")
print(results)