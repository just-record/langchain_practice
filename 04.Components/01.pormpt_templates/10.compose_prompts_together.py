from langchain_core.prompts import PromptTemplate

### 1. String prompt composition

prompt = (
    PromptTemplate.from_template("Tell me a joke about {topic}")
    + ", make it funny"
    + "\n\nand in {language}"
)

print(prompt)
# input_variables=['language', 'topic'] template='Tell me a joke about {topic}, make it funny\n\nand in {language}'

print('-'*30)
print(prompt.format(topic="sports", language="spanish"))
# Tell me a joke about sports, make it funny

# and in spanish


### 2. Chat prompt composition
print('-'*30)
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

prompt = SystemMessage(content="You are a nice pirate")
new_prompt = (
    prompt + HumanMessage(content="hi") + AIMessage(content="what?") + "{input}"
)
print(new_prompt.format_messages(input="i said hi"))
# [SystemMessage(content='You are a nice pirate'), HumanMessage(content='hi'), AIMessage(content='what?'), HumanMessage(content='i said hi')]


### 3. Using PipelinePrompt
print('-'*30)
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

print(pipeline_prompt.input_variables)
# ['example_q', 'person', 'example_a', 'input']

print('-'*30)
print(
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
