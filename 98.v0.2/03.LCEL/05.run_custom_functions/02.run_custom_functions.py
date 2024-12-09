from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import chain
from langchain_openai import ChatOpenAI

prompt1 = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
prompt2 = ChatPromptTemplate.from_template("What is the subject of this joke: {joke}")


@chain
def custom_chain(text):
    prompt_val1 = prompt1.invoke({"topic": text})       # {"topic": "bears"} => "Tell me a joke about bears"
    output1 = ChatOpenAI().invoke(prompt_val1)          # content='Why do bears have hairy coats?\n\nFur protection!' response_metadata=...
    parsed_output1 = StrOutputParser().invoke(output1)  # Why do bears have hairy coats?\n\nFur protection!
    chain2 = prompt2 | ChatOpenAI() | StrOutputParser() 
    return chain2.invoke({"joke": parsed_output1})      # What is the subject of this joke: {joke} => What is the subject of this joke: Why do bears have hairy coats?\n\nFur protection! 


results = custom_chain.invoke("bears")
print(results)  # Bears