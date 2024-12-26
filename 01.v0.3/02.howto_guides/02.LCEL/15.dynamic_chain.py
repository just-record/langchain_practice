from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI
# from langchain_anthropic import ChatAnthropic

llm = ChatOpenAI(model="gpt-4o-mini")
# llm = ChatAnthropic(model="claude-3-sonnet-20240229")


from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnablePassthrough, chain

contextualize_instructions = """Convert the latest user question into a standalone question given the chat history. Don't answer the question, return the question and nothing else (no descriptive text)."""
contextualize_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_instructions),
        ("placeholder", "{chat_history}"),
        ("human", "{question}"),
    ]
)
contextualize_question = contextualize_prompt | llm | StrOutputParser()

qa_instructions = (
    """Answer the user question given the following context:\n\n{context}."""
)
qa_prompt = ChatPromptTemplate.from_messages(
    [("system", qa_instructions), ("human", "{question}")]
)


@chain
def contextualize_if_needed(input_: dict) -> Runnable:
    if input_.get("chat_history"):
        # NOTE: This is returning another Runnable, not an actual output.
        return contextualize_question
    else:
        return RunnablePassthrough() | itemgetter("question")


@chain
def fake_retriever(input_: dict) -> str:
    return "egypt's population in 2024 is about 111 million"


full_chain = (
    RunnablePassthrough.assign(question=contextualize_if_needed).assign(
        context=fake_retriever
    )
    | qa_prompt
    | llm
    | StrOutputParser()
)

##################################################################################
### 1. chat_history가 있어서 contextualize_question를 return
print('1.', '-' * 50)
##################################################################################
results = full_chain.invoke(
    {
        "question": "what about egypt",
        "chat_history": [
            ("human", "what's the population of indonesia"),
            ("ai", "about 276 million"),
        ],
    }
)
rprint(results)
# 1. --------------------------------------------------
# As of 2024, Egypt's population is about 111 million. However, my training only includes data up to October 2023, so I cannot provide the most current figures beyond that point.

##################################################################################
### 2. contextualize_if_needed만 stream하기
### RunnablePassthrough() | itemgetter("question") 를 return하기
print('2.', '-' * 50)
##################################################################################
for chunk in contextualize_if_needed.stream(
    {
        "question": "what about egypt",
        "chat_history": [
            ("human", "what's the population of indonesia"),
            ("ai", "about 276 million"),
        ],
    }
):
    print(chunk)
# 2. --------------------------------------------------

# what
# 's
#  the
#  population
#  of
#  Egypt
# ?

