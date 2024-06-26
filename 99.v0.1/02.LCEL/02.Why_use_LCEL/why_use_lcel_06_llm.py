################################################################################
# without LCEL
################################################################################

# import openai

# prompt_template = "Tell me a short joke about {topic}"
# client = openai.OpenAI()

# def call_llm(prompt_value: str) -> str:
#     response = client.completions.create(
#         model="gpt-3.5-turbo-instruct",
#         prompt=prompt_value,
#     )
#     return response.choices[0].text

# def invoke_llm_chain(topic: str) -> str:
#     prompt_value = prompt_template.format(topic=topic)
#     return call_llm(prompt_value)

# print(invoke_llm_chain("ice cream"))
   
################################################################################
# with LCEL
################################################################################

from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

prompt = ChatPromptTemplate.from_template("tell me a short joke about {topic}")

llm = OpenAI(model='gpt-3.5-turbo-instruct')

output_parset = StrOutputParser()

llm_chain = (
    {"topic": RunnablePassthrough()}
    | prompt
    | llm
    | output_parset
)

print(llm_chain.invoke("ice cream"))