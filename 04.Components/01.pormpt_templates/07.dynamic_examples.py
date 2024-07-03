from dotenv import load_dotenv
load_dotenv()

from langchain_chroma import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings

examples = [
    {"input": "2+2", "output": "4"},
    {"input": "2+3", "output": "5"},
    {"input": "2+4", "output": "6"},
    {"input": "What did the cow say to the moon?", "output": "nothing at all"},
    {
        "input": "Write me a poem about the moon",
        "output": "One for the moon, and one for me, who are we to talk about the moon?",
    },
]

to_vectorize = [" ".join(example.values()) for example in examples]
print(to_vectorize)
# ['2+2 4', '2+3 5', '2+4 6', 'What did the cow say to the moon? nothing at all', 'Write me a poem about the moon One for the moon, and one for me, who are we to talk about the moon?']
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=examples)


### Create the example_selector
print('-'*30)

example_selector = SemanticSimilarityExampleSelector(
    vectorstore=vectorstore,
    k=2,
)
# The prompt template will load examples by passing the input do the `select_examples` method
print(example_selector.select_examples({"input": "horse"}))


### Create prompt template
print('-'*30)

from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

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

print(few_shot_prompt.invoke(input="What's 3+3?").to_messages())
# What's 3+3?과 가장 유사한 예제 2개를 반환
# [HumanMessage(content='2+3'), AIMessage(content='5'), HumanMessage(content='2+2'), AIMessage(content='4')]

print('-'*30)
final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a wondrous wizard of math."),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)

print(few_shot_prompt.invoke(input="What's 3+3?"))
# messages=[HumanMessage(content='2+3'), AIMessage(content='5'), HumanMessage(content='2+2'), AIMessage(content='4')]

### Use with an chat model
print('-'*30)
from langchain_openai import ChatOpenAI

chain = final_prompt | ChatOpenAI(model="gpt-3.5-turbo", temperature=0.0)
print(chain.invoke({"input": "What's 3+3?"}))
# content='6' ...