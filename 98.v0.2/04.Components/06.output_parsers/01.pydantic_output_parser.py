from dotenv import load_dotenv
load_dotenv()

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_openai import OpenAI

model = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0.0)


# Define your desired data structure.
class Joke(BaseModel):
    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")

    # You can add custom validation logic easily with Pydantic.
    @validator("setup")
    def question_ends_with_question_mark(cls, field):
        if field[-1] != "?":
            raise ValueError("Badly formed question!")
        return field


# Set up a parser + inject instructions into the prompt template.
parser = PydanticOutputParser(pydantic_object=Joke)
print(f'parser.get_format_instructions(): {parser.get_format_instructions()}')
print('-'*30)
# parser.get_format_instructions(): The output should be formatted as a JSON instance that conforms to the JSON schema below.

# As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
# the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

# Here is the output schema:
# ```
# {"properties": {"setup": {"title": "Setup", "description": "question to set up a joke", "type": "string"}, "punchline": {"title": "Punchline", "description": "answer to resolve the joke", "type": "string"}}, "required": ["setup", "punchline"]}
# ```

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# And a query intended to prompt a language model to populate the data structure.
prompt_and_model = prompt | model
### 1. output parser를 사용 하지 않고.
output = prompt_and_model.invoke({"query": "Tell me a joke."})
print(output)

# {
#     "setup": "Why did the tomato turn red?",
#     "punchline": "Because it saw the salad dressing!"
# }


### 2. Output parsers implement the Runnable interface
print('-'*30)
print(parser.invoke(output))
# setup='Why did the tomato turn red?' punchline='Because it saw the salad dressing!'


### 3. parser를 적용
print('-'*30)
chain = prompt | model | parser
results = chain.invoke({"query": "Tell me a joke."})
print(results)
# setup='Why did the tomato turn red?' punchline='Because it saw the salad dressing!'


### 4. SimpleJsonOutputParser 를 적용 - stream 적용 가능
print('-'*30)
from langchain.output_parsers.json import SimpleJsonOutputParser

json_prompt = PromptTemplate.from_template(
    "Return a JSON object with an `answer` key that answers the following question: {question}"
)
json_parser = SimpleJsonOutputParser()
json_chain = json_prompt | model | json_parser
results = json_chain.stream({"question": "Who invented the microscope?"})
for result in results:
    print(result)
# {}
# {'answer': ''}
# {'answer': 'Ant'}
# {'answer': 'Anton'}
# {'answer': 'Antonie'}
# {'answer': 'Antonie van'}
# {'answer': 'Antonie van Lee'}
# {'answer': 'Antonie van Leeu'}
# {'answer': 'Antonie van Leeuwen'}
# {'answer': 'Antonie van Leeuwenho'}
# {'answer': 'Antonie van Leeuwenhoek'}    


### 4. 'PydanticOutputParser'는 stream 이 불가능 => 모든 출력 파서가 stream을 지원하지 않음
print('-'*30)
## 아래 코드는 실행는 오류 발생 => langchain_core.exceptions.OutputParserException: Invalid json output: 
# print(list(chain.stream({"query": "Tell me a joke."})))
