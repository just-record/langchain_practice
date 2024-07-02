from dotenv import load_dotenv
load_dotenv()

# from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

chain = (
    PromptTemplate.from_template(
        """Given the user question below, classify it as either being about `LangChain`, `Anthropic`, or `Other`.

Do not respond with more than one word.

<question>
{question}
</question>

Classification:"""
    )
    # | ChatAnthropic(model_name="claude-3-haiku-20240307")
    | ChatOpenAI(model_name="gpt-3.5-turbo")
    | StrOutputParser()
)

# results = chain.invoke({"question": "how do I call Anthropic?"})
# print(results)


langchain_chain = PromptTemplate.from_template(
    """You are an expert in langchain. \
Always answer questions starting with "As Harrison Chase told me". \
Respond to the following question:

Question: {question}
Answer:"""
) | ChatOpenAI(model_name="gpt-3.5-turbo")


anthropic_chain = PromptTemplate.from_template(
    """You are an expert in anthropic. \
Always answer questions starting with "As Dario Amodei told me". \
Respond to the following question:

Question: {question}
Answer:"""
) | ChatOpenAI(model_name="gpt-3.5-turbo")


general_chain = PromptTemplate.from_template(
    """Respond to the following question:

Question: {question}
Answer:"""
) | ChatOpenAI(model_name="gpt-3.5-turbo")


def route(info):
    if "anthropic" in info["topic"].lower():
        return anthropic_chain
    elif "langchain" in info["topic"].lower():
        return langchain_chain
    else:
        return general_chain
    

from langchain_core.runnables import RunnableLambda

full_chain = {"topic": chain, "question": lambda x: x["question"]} | RunnableLambda(route)

### 1. Anthropic 질의
results = full_chain.invoke({"question": "how do I use Anthropic?"})
print(results)
# 출력: As Dario Amodei told me
# content='As Dario Amodei told me, the Anthropic framework can be used to analyze the relationship between intelligent agents and their environment, as well as to understand the impact of human behavior on the world. It can also be applied to various fields such as artificial intelligence, ethics, and decision-making.' response_metadata={'token_usage': {'completion_tokens': 60, 'prompt_tokens': 47, 'total_tokens': 107}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-4a39506d-4740-471d-9c42-730979237285-0' usage_metadata={'input_tokens': 47, 'output_tokens': 60, 'total_tokens': 107}
print('-'*30)

### 2. LangChain 질의: As Harrison Chase told me
results = full_chain.invoke({"question": "how do I use LangChain?"})
print(results)
# 출력
# content='As Harrison Chase told me, to use LangChain, you first need to create an account on the platform. Then, you can browse through the available language learning courses and select the one that interests you. From there, you can follow the lessons, complete the activities, and practice using the language with other users on the platform.' response_metadata={'token_usage': {'completion_tokens': 66, 'prompt_tokens': 44, 'total_tokens': 110}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-6a345cd7-6a1c-4812-9c84-0dcf8ca3ace9-0' usage_metadata={'input_tokens': 44, 'output_tokens': 66, 'total_tokens': 110}
print('-'*30)

### 3. 일반 질의
results = full_chain.invoke({"question": "whats 2 + 2"})
print(results)
# 출력
# content='2 + 2 equals 4.' response_metadata={'token_usage': {'completion_tokens': 8, 'prompt_tokens': 24, 'total_tokens': 32}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-0c43a5c2-15b8-4e95-9a3e-3d8c2a6d2aed-0' usage_metadata={'input_tokens': 24, 'output_tokens': 8, 'total_tokens': 32}