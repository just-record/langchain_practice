from dotenv import load_dotenv
load_dotenv()

from langchain_core.runnables import RunnableParallel, RunnablePassthrough

runnable = RunnableParallel(
    passed=RunnablePassthrough(),
    modified=lambda x: x["num"] + 1,
)

results = runnable.invoke({"num": 1})
print(results)