# pip install -qU langchain_ollama

from rich import print as rprint
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3.2")

#################################################################################
### 1. OllamaLLM
print('1.', '-' * 50)
##################################################################################
rprint(llm.invoke("The first man on the moon was ..."))
# 1. --------------------------------------------------
# ...Neil Armstrong. He stepped onto the lunar surface on July 20, 1969, as part of the Apollo 11 mission.


#################################################################################
### 2. OllamaLLM - stream
print('2.', '-' * 50)
##################################################################################
for chunk in llm.stream("The first man on the moon was ..."):
    print(chunk, end="|", flush=True)
# 2. --------------------------------------------------
# Neil| Armstrong|.| He| made| history| by| becoming| the| first| person| to| set| foot| on| the| Moon| on| July| |20|,| |196|9|,| during| the| Apollo| |11| mission|.||


#################################################################################
### 3. ChatOllama
print('3.', '-' * 50)
##################################################################################
from langchain_ollama import ChatOllama

chat_model = ChatOllama(model="llama3.2")

rprint(chat_model.invoke("Who was the first man on the moon?"))
# 3. --------------------------------------------------
# AIMessage(
#     content='The first man to set foot on the Moon was Neil Armstrong. He stepped onto the lunar surface on July 20, 1969 as part of the Apollo 11 mission.',
#     additional_kwargs={},
#     response_metadata={
#         'model': 'llama3.2',
#         'created_at': '2025-01-02T07:50:27.942925756Z',
#         'done': True,
#         'done_reason': 'stop',
#         'total_duration': 1888641121,
#         'load_duration': 9823768,
#         'prompt_eval_count': 34,
#         'prompt_eval_duration': 163000000,
#         'eval_count': 37,
#         'eval_duration': 1714000000,
#         'message': Message(role='assistant', content='', images=None, tool_calls=None)
#     },
#     id='run-b0ed775e-6204-4342-97c3-0916323d6622-0',
#     usage_metadata={'input_tokens': 34, 'output_tokens': 37, 'total_tokens': 71}
# )


#################################################################################
### 4. 일부 LLM은 특정 프롬프트를 통해 더 나은 성능을 발휘
### LLaMA는 특수 토큰을 사용
print('4.', '-' * 50)
##################################################################################
from langchain.chains.prompt_selector import ConditionalPromptSelector
from langchain_core.prompts import PromptTemplate

llm = OllamaLLM(model="llama3.2")

DEFAULT_LLAMA_SEARCH_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""<<SYS>> \n You are an assistant tasked with improving Google search \
results. \n <</SYS>> \n\n [INST] Generate THREE Google search queries that \
are similar to this question. The output should be a numbered list of questions \
and each should have a question mark at the end: \n\n {question} [/INST]""",
)

DEFAULT_SEARCH_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""You are an assistant tasked with improving Google search \
results. Generate THREE Google search queries that are similar to \
this question. The output should be a numbered list of questions and each \
should have a question mark at the end: {question}""",
)

QUESTION_PROMPT_SELECTOR = ConditionalPromptSelector(
    default_prompt=DEFAULT_SEARCH_PROMPT,
    conditionals=[(lambda llm: isinstance(llm, OllamaLLM), DEFAULT_LLAMA_SEARCH_PROMPT)],
)

prompt = QUESTION_PROMPT_SELECTOR.get_prompt(llm)
rprint(prompt)
# 4. --------------------------------------------------
# PromptTemplate(
#     input_variables=['question'],
#     input_types={},
#     partial_variables={},
#     template='<<SYS>> \n You are an assistant tasked with improving Google search results. \n <</SYS>> \n\n [INST] Generate THREE Google search queries that are similar to this question. The output should be a
# numbered list of questions and each should have a question mark at the end: \n\n {question} [/INST]'
# )


# Chain
print(' ')
chain = prompt | llm
question = "What NFL team won the Super Bowl in the year that Justin Bieber was born?"
rprint(chain.invoke({"question": question}))
# Here are three similar Google search queries:

# 1. What NFL team won the Super Bowl in 1994?
# 2. Which NFL team has won the most Super Bowls since the year 2000?
# 3. Who won the Super Bowl in the year that Tom Brady was born?