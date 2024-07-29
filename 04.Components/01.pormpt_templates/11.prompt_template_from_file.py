from langchain.prompts import load_prompt


file_path_prompt = './prompt_basic.yaml'

prompt_template = load_prompt(file_path_prompt)
print(prompt_template.invoke({"topic": "cats"}).to_messages())
# [HumanMessage(content='Tell me a joke about cats')]
