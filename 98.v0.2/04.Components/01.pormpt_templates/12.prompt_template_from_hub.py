from langchain import hub

prompt_template = hub.pull("jbsh/langchain_practice_basic", api_url="https://api.hub.langchain.com")
print(prompt_template)
# input_variables=['topic'] metadata={'lc_hub_owner': 'jbsh', 'lc_hub_repo': 'langchain_practice_basic', 'lc_hub_commit_hash': '240f00963407c13026b1e00d32990a5e3117e63d47a911f02ec3fe3a77d7e543'} messages=[SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], template='You are a chatbot.')), HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['topic'], template='Tell me a joke about {topic}'))]
print('-'*30)
print(prompt_template.invoke({"topic": "cats"}).to_messages())
# [SystemMessage(content='You are a chatbot.'), HumanMessage(content='Tell me a joke about cats')]
