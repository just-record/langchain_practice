from rich import print as rprint

from langchain_core.prompts import PromptTemplate


#################################################################################
### 1. 문자열 Prompt 구성하기
print('1.', '-' * 50)
##################################################################################
prompt = (
    PromptTemplate.from_template("Tell me a joke about {topic}")
    + ", make it funny"
    + "\n\nand in {language}"
)

rprint(prompt)
# PromptTemplate(input_variables=['language', 'topic'], input_types={}, partial_variables={}, template='Tell me a joke about {topic}, make it funny\n\nand in {language}')

print(" ")
rprint(prompt.format(topic="sports", language="spanish"))
# Tell me a joke about sports, make it funny

# and in spanish

print(" ")
rprint(prompt.invoke({"topic": "sports", "language": "spanish"}))
# StringPromptValue(text='Tell me a joke about sports, make it funny\n\nand in spanish')


#################################################################################
### 2. Chat Prompt 구성하기
print('2.', '-' * 50)
##################################################################################
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

prompt = SystemMessage(content="You are a nice pirate")

new_prompt = (
    prompt + HumanMessage(content="hi") + AIMessage(content="what?") + "{input}"
)

rprint(new_prompt.format_messages(input="i said hi"))
# 2. --------------------------------------------------
# [
#     SystemMessage(content='You are a nice pirate', additional_kwargs={}, response_metadata={}),
#     HumanMessage(content='hi', additional_kwargs={}, response_metadata={}),
#     AIMessage(content='what?', additional_kwargs={}, response_metadata={}),
#     HumanMessage(content='i said hi', additional_kwargs={}, response_metadata={})
# ]


#################################################################################
### 3. Pipeline Prompt 사용
print('3.', '-' * 50)
##################################################################################
from langchain_core.prompts import PipelinePromptTemplate, PromptTemplate

full_template = """{introduction}

{example}

{start}"""
full_prompt = PromptTemplate.from_template(full_template)

introduction_template = """You are impersonating {person}."""
introduction_prompt = PromptTemplate.from_template(introduction_template)

example_template = """Here's an example of an interaction:

Q: {example_q}
A: {example_a}"""
example_prompt = PromptTemplate.from_template(example_template)

start_template = """Now, do this for real!

Q: {input}
A:"""
start_prompt = PromptTemplate.from_template(start_template)

input_prompts = [
    ("introduction", introduction_prompt),
    ("example", example_prompt),
    ("start", start_prompt),
]
pipeline_prompt = PipelinePromptTemplate(
    final_prompt=full_prompt, pipeline_prompts=input_prompts
)

rprint(pipeline_prompt.input_variables)
# 3. --------------------------------------------------
# ['person', 'example_q', 'input', 'example_a']

print(" ")
rprint(pipeline_prompt)
# PipelinePromptTemplate(
#     input_variables=['input', 'person', 'example_a', 'example_q'],
#     input_types={},
#     partial_variables={},
#     final_prompt=PromptTemplate(input_variables=['example', 'introduction', 'start'], input_types={}, partial_variables={}, template='{introduction}\n\n{example}\n\n{start}'),
#     pipeline_prompts=[
#         ('introduction', PromptTemplate(input_variables=['person'], input_types={}, partial_variables={}, template='You are impersonating {person}.')),
#         ('example', PromptTemplate(input_variables=['example_a', 'example_q'], input_types={}, partial_variables={}, template="Here's an example of an interaction:\n\nQ: {example_q}\nA: {example_a}")),
#         ('start', PromptTemplate(input_variables=['input'], input_types={}, partial_variables={}, template='Now, do this for real!\n\nQ: {input}\nA:'))
#     ]
# )

print(" ")
rprint(
    pipeline_prompt.format(
        person="Elon Musk",
        example_q="What's your favorite car?",
        example_a="Tesla",
        input="What's your favorite social media site?",
    )
)
# You are impersonating Elon Musk.

# Here's an example of an interaction:

# Q: What's your favorite car?
# A: Tesla

# Now, do this for real!

# Q: What's your favorite social media site?
# A:


print(" ")
rprint(
    pipeline_prompt.invoke(
        {
            "person": "Elon Musk",
            "example_q": "What's your favorite car?",
            "example_a": "Tesla",
            "input": "What's your favorite social media site?",
        }
    )
)
# StringPromptValue(text="You are impersonating Elon Musk.\n\nHere's an example of an interaction:\n\nQ: What's your favorite car?\nA: Tesla\n\nNow, do this for real!\n\nQ: What's your favorite social media site?\nA:")