from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate


examples = [
    {"input": "2+2", "output": "4"},
    {"input": "2+3", "output": "5"},
]

example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}"),
        ("ai", "{output}"),
    ]
)

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)


print(few_shot_prompt.invoke({}).to_messages())
# [HumanMessage(content='2+2'), AIMessage(content='4'), HumanMessage(content='2+3'), AIMessage(content='5')]

### llm에 적용하기
print('-'*30)

final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a wondrous wizard of math."),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

chain = final_prompt | ChatOpenAI(model="gpt-3.5-turbo", temperature=0.0)

results = chain.invoke({"input": "What's the square of a triangle?"})
print(results)
# content='A triangle does not have a square. The square is a shape with four equal sides and four right angles, while a triangle has three sides and three angles.' response_metadata={'token_usage': {'completion_tokens': 32, 'prompt_tokens': 52, 'total_tokens': 84}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-7cf1415f-97a0-434c-be80-8cad0a7572ee-0' usage_metadata={'input_tokens': 52, 'output_tokens': 32, 'total_tokens': 84}