#################################################################################
### 전체 예제 세트에서 일부 예제만을 선택
### example_selector: 예제의 일부만 FewShotPromptTemplate에 사용
### example_prompt: 각 예시를 하나 이상의 메시지로 변환
### SemanticSimilarityExampleSelector: 의미적 유사성을 기반으로 예시를 선택 
#################################################################################
from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI

from langchain_chroma import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings

model = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

examples = [
    {"input": "2 🦜 2", "output": "4"},
    {"input": "2 🦜 3", "output": "5"},
    {"input": "2 🦜 4", "output": "6"},
    {"input": "What did the cow say to the moon?", "output": "nothing at all"},
    {
        "input": "Write me a poem about the moon",
        "output": "One for the moon, and one for me, who are we to talk about the moon?",
    },
]

to_vectorize = [" ".join(example.values()) for example in examples]
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=examples)

#################################################################################
### 1. example_selector 생성 및 select 해보기
print('1.', '-' * 50)
##################################################################################
example_selector = SemanticSimilarityExampleSelector(
    vectorstore=vectorstore,
    k=2,
)

# The prompt template will load examples by passing the input do the `select_examples` method
rprint(example_selector.select_examples({"input": "horse"}))
# 1. --------------------------------------------------
# [{'input': 'What did the cow say to the moon?', 'output': 'nothing at all'}, {'input': '2 🦜 4', 'output': '6'}]


#################################################################################
### 2. example_selector - prompt에 적용
print('2.', '-' * 50)
##################################################################################
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

# Define the few-shot prompt.
few_shot_prompt = FewShotChatMessagePromptTemplate(
    # The input variables select the values to pass to the example_selector
    input_variables=["input"],
    example_selector=example_selector,
    # Define how each example will be formatted.
    # In this case, each example will become 2 messages:
    # 1 human, and 1 AI
    example_prompt=ChatPromptTemplate.from_messages(
        [("human", "{input}"), ("ai", "{output}")]
    ),
)

rprint(few_shot_prompt.invoke(input="What's 3 🦜 3?").to_messages())
# 2. --------------------------------------------------
# [
#     HumanMessage(content='2 🦜 3', additional_kwargs={}, response_metadata={}),
#     AIMessage(content='5', additional_kwargs={}, response_metadata={}),
#     HumanMessage(content='2 🦜 4', additional_kwargs={}, response_metadata={}),
#     AIMessage(content='6', additional_kwargs={}, response_metadata={})
# ]


#################################################################################
### 3. example_selector - chat model에 적용
print('3.', '-' * 50)
##################################################################################
final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a wondrous wizard of math."),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)

rprint(few_shot_prompt.invoke(input="What's 3 🦜 3?"))
# 3. --------------------------------------------------
# ChatPromptValue(
#     messages=[
#         HumanMessage(content='2 🦜 3', additional_kwargs={}, response_metadata={}),
#         AIMessage(content='5', additional_kwargs={}, response_metadata={}),
#         HumanMessage(content='2 🦜 4', additional_kwargs={}, response_metadata={}),
#         AIMessage(content='6', additional_kwargs={}, response_metadata={})
#     ]
# )

print('')
chain = final_prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

rprint(chain.invoke({"input": "What's 3 🦜 3?"}))
# AIMessage(
#     content='3 🦜 3 equals 6.',
#     additional_kwargs={'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 11,
#             'prompt_tokens': 59,
#             'total_tokens': 70,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-mini-2024-07-18',
#         'system_fingerprint': 'fp_d02d531b47',
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-13442a52-703a-4306-b277-208ef8331857-0',
#     usage_metadata={'input_tokens': 59, 'output_tokens': 11, 'total_tokens': 70, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )