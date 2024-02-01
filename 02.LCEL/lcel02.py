# Prompt

from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("tell me a short joke about {topic}")

prompt_value = prompt.invoke({"topic": "ice cream"})
print(type(prompt_value))

print(prompt_value)
# ChatPromptValue(messages=[HumanMessage(content='tell me a short joke about ice cream')])

print(prompt_value.to_messages())
# [HumanMessage(content='tell me a short joke about ice cream')]

print(prompt_value.to_string())
# 'Human: tell me a short joke about ice cream'