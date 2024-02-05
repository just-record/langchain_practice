### Anthropic: 인공지능 회사. API Key를 발급 받아야 해서 일단 생략

################################################################################
# without LCEL
################################################################################

# import anthropic

# prompt_template = "Tell me a short joke about {topic}"

# anthropic_template = f"Human:\n\n{prompt_template}\n\nAssistant:"
# anthropic_client = anthropic.Anthropic()

# def call_anthropic(prompt_value: str) -> str:
#     response = anthropic_client.completions.create(
#         model="claude-2",
#         prompt=prompt_value,
#         max_tokens_to_sample=256,
#     )
#     return response.completion    

# def invoke_anthropic_chain(topic: str) -> str:
#     prompt_value = anthropic_template.format(topic=topic)
#     return call_anthropic(prompt_value)

# invoke_anthropic_chain("ice cream")
   
################################################################################
# with LCEL
################################################################################

# from langchain_core.output_parsers import StrOutputParser
# # from langchain_openai import OpenAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.runnables import RunnablePassthrough
# from langchain_community.chat_models import ChatAnthropic

# prompt = ChatPromptTemplate.from_template("tell me a short joke about {topic}")

# anthropic = ChatAnthropic(model="claude-2")
# # llm = OpenAI(model='gpt-3.5-turbo-instruct')

# output_parset = StrOutputParser()

# anthropic_chain = (
#     {"topic": RunnablePassthrough()}
#     | prompt
#     | anthropic
#     | output_parset
# )

# print(anthropic_chain.invoke("ice cream"))