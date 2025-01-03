### 출력 파서(Output parser)는 언어 모델 응답을 구조화하는 데 도움을 주는 클래스

from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint


#################################################################################
### 1. PydanticOutputParser의 예시
print('1.', '-' * 50)
##################################################################################
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from pydantic import BaseModel, Field, model_validator

model = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0.0)


# Define your desired data structure.
class Joke(BaseModel):
    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")

    # You can add custom validation logic easily with Pydantic.
    @model_validator(mode="before")
    @classmethod
    def question_ends_with_question_mark(cls, values: dict) -> dict:
        setup = values.get("setup")
        if setup and setup[-1] != "?":
            raise ValueError("Badly formed question!")
        return values


# Set up a parser + inject instructions into the prompt template.
parser = PydanticOutputParser(pydantic_object=Joke)

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# And a query intended to prompt a language model to populate the data structure.
prompt_and_model = prompt | model
output = prompt_and_model.invoke({"query": "Tell me a joke."})
results = parser.invoke(output)
rprint(results)
# 1. --------------------------------------------------
# Joke(setup='Why did the tomato turn red?', punchline='Because it saw the salad dressing!')

################## 추가로 이것 저것 해 보기 ##################
### dictionary로 변환 ###
print(' ')
results_dict = results.dict()
rprint(type(results_dict))
rprint(results_dict)
# <class 'dict'>
# {'setup': 'Why did the tomato turn red?', 'punchline': 'Because it saw the salad dressing!'}

### prompt만 invoke ###
print(' ')
rprint(prompt.invoke({"query": "Tell me a joke."}))
# StringPromptValue(
#     text='Answer the user query.\nThe output should be formatted as a JSON instance that conforms to the JSON schema below.\n\nAs an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of 
# strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}\nthe object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not 
# well-formatted.\n\nHere is the output schema:\n```\n{"properties": {"setup": {"description": "question to set up a joke", "title": "Setup", "type": "string"}, "punchline": {"description": "answer to resolve the joke", "title":
# "Punchline", "type": "string"}}, "required": ["setup", "punchline"]}\n```\nTell me a joke.\n'
# )

### output 출력 ###
print(' ')
rprint(type(output))
rprint(output)
# <class 'str'>
# {"setup": "Why did the tomato turn red?", "punchline": "Because it saw the salad dressin


#################################################################################
### 2. LCEL - Output parser invoke
### Output parser는 Runnable interface를 구현(the basic building block of LCEL)
### invoke, ainvoke, stream, astream, batch, abatch, astream_log 가능
print('2.', '-' * 50)
##################################################################################
rprint(parser.invoke(output))
# 2. --------------------------------------------------
# Joke(setup='Why did the tomato turn red?', punchline='Because it saw the salad dressing!')


#################################################################################
### 3. LCEL - Output parser를 chaining
print('3.', '-' * 50)
##################################################################################
chain = prompt | model | parser
rprint(chain.invoke({"query": "Tell me a joke."}))
# 3. --------------------------------------------------
# Joke(setup='Why did the tomato turn red?', punchline='Because it saw the salad dressing!')


#################################################################################
### 4. LCEL - 스트리밍 인터페이스 - SimpleJsonOutputParser 예시
### 부분적으로 파싱된 객체를 스트리밍하는 것은 출력 유형에 크게 의존하기 때문에 특정 파서만 가능
### 부분 객체를 구성할 수 없는 파서는 단순히 완전히 파싱된 출력을 생성합니다.
print('4.', '-' * 50)
##################################################################################
from langchain.output_parsers.json import SimpleJsonOutputParser

json_prompt = PromptTemplate.from_template(
    "Return a JSON object with an `answer` key that answers the following question: {question}"
)
json_parser = SimpleJsonOutputParser()
json_chain = json_prompt | model | json_parser

rprint(list(json_chain.stream({"question": "Who invented the microscope?"})))
# 4. --------------------------------------------------
# [
#     {},
#     {'answer': ''},
#     {'answer': 'Ant'},
#     {'answer': 'Anton'},
#     {'answer': 'Antonie'},
#     {'answer': 'Antonie van'},
#     {'answer': 'Antonie van Lee'},
#     {'answer': 'Antonie van Leeu'},
#     {'answer': 'Antonie van Leeuwen'},
#     {'answer': 'Antonie van Leeuwenho'},
#     {'answer': 'Antonie van Leeuwenhoek'}
# ]


#################################################################################
### 5. LCEL - 스트리밍 인터페이스 - PydanticOutputParser 예시
### 부분적으로 파싱된 객체를 스트리밍하는 것은 출력 유형에 크게 의존하기 때문에 특정 파서만 가능
### 부분 객체를 구성할 수 없는 파서는 단순히 완전히 파싱된 출력을 생성합니다.
print('5.', '-' * 50)
##################################################################################
rprint(list(chain.stream({"query": "Tell me a joke."})))
# 5. --------------------------------------------------
# [
#     Joke(setup='Why did the tomato turn red?', punchline=''),
#     Joke(setup='Why did the tomato turn red?', punchline='Because'),
#     Joke(setup='Why did the tomato turn red?', punchline='Because it'),
#     Joke(setup='Why did the tomato turn red?', punchline='Because it saw'),
#     Joke(setup='Why did the tomato turn red?', punchline='Because it saw the'),
#     Joke(setup='Why did the tomato turn red?', punchline='Because it saw the salad'),
#     Joke(setup='Why did the tomato turn red?', punchline='Because it saw the salad dressing'),
#     Joke(setup='Why did the tomato turn red?', punchline='Because it saw the salad dressing!')
# ]