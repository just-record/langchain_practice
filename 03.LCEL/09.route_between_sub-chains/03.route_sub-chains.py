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


from langchain_core.runnables import RunnableBranch

branch = RunnableBranch(
    (lambda x: "anthropic" in x["topic"].lower(), anthropic_chain),
    (lambda x: "langchain" in x["topic"].lower(), langchain_chain),
    general_chain,
)
full_chain = {"topic": chain, "question": lambda x: x["question"]} | branch
full_chain.invoke({"question": "how do I use Anthropic?"})

full_chain = {"topic": chain, "question": lambda x: x["question"]} | branch

### 1. Anthropic 질의
results = full_chain.invoke({"question": "how do I use Anthropic?"})
print(results)
# 출력: As Dario Amodei told me
# content='As Dario Amodei told me, using Anthropic involves understanding and applying principles of the anthropic reasoning framework to analyze and interpret phenomena in the universe in relation to the presence of human observers. This can involve considering how certain physical constants and conditions in the universe are fine-tuned to allow for the existence of intelligent life like us.' response_metadata={'token_usage': {'completion_tokens': 68, 'prompt_tokens': 47, 'total_tokens': 115}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-2ca8ea8f-09da-457b-9cb9-d84ae8b0ecec-0' usage_metadata={'input_tokens': 47, 'output_tokens': 68, 'total_tokens': 115}
print('-'*30)

### 2. LangChain 질의: As Harrison Chase told me
results = full_chain.invoke({"question": "how do I use LangChain?"})
print(results)
# 출력
# content='As Harrison Chase told me, to use LangChain, you first need to create an account on the platform. Once you have registered, you can start using LangChain to connect with language experts, schedule lessons, and track your progress in learning a new language.' response_metadata={'token_usage': {'completion_tokens': 52, 'prompt_tokens': 44, 'total_tokens': 96}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-780b21d7-1f8d-43a5-a1aa-76a34db8cb8b-0' usage_metadata={'input_tokens': 44, 'output_tokens': 52, 'total_tokens': 96}
print('-'*30)

### 3. 일반 질의
results = full_chain.invoke({"question": "whats 2 + 2"})
print(results)
# 출력 content='2 + 2 equals 4.' response_metadata={'token_usage': {'completion_tokens': 8, 'prompt_tokens': 24, 'total_tokens': 32}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-5dcfbc03-42d1-40e8-8857-a515d69cb1cf-0' usage_metadata={'input_tokens': 24, 'output_tokens': 8, 'total_tokens': 32}
# print('-'*30)