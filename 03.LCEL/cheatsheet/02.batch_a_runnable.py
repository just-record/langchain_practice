# from langchain.globals import set_debug, get_debug
# set_debug(False)

from langchain_core.runnables import RunnableLambda

runnable = RunnableLambda(lambda x: str(x))
print(runnable.batch([7, 8, 9]))
# ['7', '8', '9']

# Async variant:
# await runnable.abatch([7, 8, 9])

### Batch로 처리 할 때 llm까지 연결 하면?
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

llm = ChatOpenAI(model="gpt-3.5-turbo")
template = "Whats the next number: {number}"
prompt = ChatPromptTemplate.from_template(template)

chain = runnable | {"number": RunnablePassthrough()} | prompt | llm

results = chain.batch([7, 8, 9])
for result in results:
    print(result.content)
# The next number is 8.
# The next number after 8 is 9.
# The next number after 9 is 10.    
