from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnablePassthrough, chain


llm = ChatOpenAI(model="gpt-3.5-turbo")


contextualize_instructions = """Convert the latest user question into a standalone question given the chat history. 
Don't answer the question, return the question and nothing else (no descriptive text)."""


contextualize_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_instructions),
        ("placeholder", "{chat_history}"),
        ("human", "{question}"),
    ]
)


# 'contextualize_question'는 Runnable이지 실제 실행 되지 않는다. 나중에 invoke() 또는 stream()을 호출할 때 실행된다.
# 'chat_history' 형태의 독립된 질문을 생성 하여 반환 한다.(기존의 chat_history에 추가 되지 않는다.)
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
        print(f'contextualize_if_needed: {input_}')
        return contextualize_question
    else:
        return RunnablePassthrough()
    

@chain
def fake_retriever(input_: dict) -> str:
    print(f'fack_retriever: {input_}')
    return "egypt's population in 2024 is about 111 million"    


full_chain = (
    RunnablePassthrough.assign(question=contextualize_if_needed).assign(
        context=fake_retriever
    )
    | qa_prompt
    | llm
    | StrOutputParser()
)


### 1. 'chat_history' 없는 경우
results = full_chain.invoke(
    {
        "question": "what about egypt",
        # "chat_history": [
        #     ("human", "what's the population of indonesia"),
        #     ("ai", "about 276 million"),
        # ],
    }
)
print(results)
# 출력
# fack_retriever: {'question': {'question': 'what about egypt'}}
# In 2024, Egypt's population is about 111 million.
print('-'*30)

### 2. 'chat_history' 있는 경우
results = full_chain.invoke(
    {
        "question": "what about egypt",
        "chat_history": [
            ("human", "what's the population of indonesia"),
            ("ai", "about 276 million"),
        ],
    }
)
print(results)
# 출력
# contextualize_if_needed: {'question': 'what about egypt', 'chat_history': [('human', "what's the population of indonesia"), ('ai', 'about 276 million')]}
# fack_retriever: {'question': 'What is the population of Egypt?', 'chat_history': [('human', "what's the population of indonesia"), ('ai', 'about 276 million')]}
# The population of Egypt in 2024 is about 111 million.
print('-'*30)

### 3. 'contextualize_if_needed'만 확인 하기
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
# 출력
# contextualize_if_needed: {'question': 'what about egypt', 'chat_history': [('human', "what's the population of indonesia"), ('ai', 'about 276 million')]}

# What
#  is
#  the
#  population
#  of
#  Egypt
# ?    