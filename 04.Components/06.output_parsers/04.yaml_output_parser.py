from dotenv import load_dotenv
load_dotenv()

from langchain.output_parsers import YamlOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI


# Define your desired data structure.
class Joke(BaseModel):
    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")


model = ChatOpenAI(temperature=0)

# And a query intented to prompt a language model to populate the data structure.
joke_query = "Tell me a joke."

# Set up a parser + inject instructions into the prompt template.
parser = YamlOutputParser(pydantic_object=Joke)
print(f'parser.get_format_instructions(): {parser.get_format_instructions()}')
print('-'*30)
# parser.get_format_instructions(): The output should be formatted as a YAML instance that conforms to the given JSON schema below.

# # Examples
# ## Schema
# ```
# {"title": "Players", "description": "A list of players", "type": "array", "items": {"$ref": "#/definitions/Player"}, "definitions": {"Player": {"title": "Player", "type": "object", "properties": {"name": {"title": "Name", "description": "Player name", "type": "string"}, "avg": {"title": "Avg", "description": "Batting average", "type": "number"}}, "required": ["name", "avg"]}}}
# ```
# ## Well formatted instance
# ```
# - name: John Doe
#   avg: 0.3
# - name: Jane Maxfield
#   avg: 1.4
# ```

# ## Schema
# ```
# {"properties": {"habit": { "description": "A common daily habit", "type": "string" }, "sustainable_alternative": { "description": "An environmentally friendly alternative to the habit", "type": "string"}}, "required": ["habit", "sustainable_alternative"]}
# ```
# ## Well formatted instance
# ```
# habit: Using disposable water bottles for daily hydration.
# sustainable_alternative: Switch to a reusable water bottle to reduce plastic waste and decrease your environmental footprint.
# ``` 

# Please follow the standard YAML formatting conventions with an indent of 2 spaces and make sure that the data types adhere strictly to the following JSON schema: 
# ```
# {"properties": {"setup": {"title": "Setup", "description": "question to set up a joke", "type": "string"}, "punchline": {"title": "Punchline", "description": "answer to resolve the joke", "type": "string"}}, "required": ["setup", "punchline"]}
# ```

# Make sure to always enclose the YAML output in triple backticks (```). Please do not add anything other than valid YAML output!

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | model | parser

results = chain.invoke({"query": joke_query})
print(results)
# setup="Why couldn't the bicycle stand up by itself?" punchline='Because it was two tired!'