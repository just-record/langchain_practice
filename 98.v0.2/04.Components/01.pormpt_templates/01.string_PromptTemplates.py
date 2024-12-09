from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template("Tell me a joke about {topic}")

results = prompt_template.invoke({"topic": "cats"})
print(results)
# text='Tell me a joke about cats'