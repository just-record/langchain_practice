from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

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
    | ChatOpenAI(model="gpt-4o-mini")
    | StrOutputParser()
)

results = chain.invoke({"question": "how do I call Anthropic?"})
print(results)


### 3개의 하위 체인 ###
langchain_chain = PromptTemplate.from_template(
    """You are an expert in langchain. \
Always answer questions starting with "As Harrison Chase told me". \
Respond to the following question:

Question: {question}
Answer:"""
) | ChatOpenAI(model="gpt-4o-mini")

anthropic_chain = PromptTemplate.from_template(
    """You are an expert in anthropic. \
Always answer questions starting with "As Dario Amodei told me". \
Respond to the following question:

Question: {question}
Answer:"""
) | ChatOpenAI(model="gpt-4o-mini")

general_chain = PromptTemplate.from_template(
    """Respond to the following question:

Question: {question}
Answer:"""
) | ChatOpenAI(model="gpt-4o-mini")


### 라우팅 사용자 함수 ###
def route(info):
    if "anthropic" in info["topic"].lower():
        return anthropic_chain
    elif "langchain" in info["topic"].lower():
        return langchain_chain
    else:
        return general_chain
    

##################################################################################
### 1. RunnableLambda로 라우팅 하기
print('1.', '-' * 50)
##################################################################################
from langchain_core.runnables import RunnableLambda

full_chain = {"topic": chain, "question": lambda x: x["question"]} | RunnableLambda(
    route
)    

results = full_chain.invoke({"question": "how do I use Anthropic?"})
rprint(results)
# 1. --------------------------------------------------
# AIMessage(
#     content="As Dario Amodei told me, using Anthropic involves understanding the specific tools and platforms they offer, such as Claude, their conversational AI model. You can interact with these models through their API, 
# which allows you to integrate AI capabilities into your applications. It's essential to familiarize yourself with their documentation, which provides guidelines on how to implement various features, manage API requests, and 
# ensure you're using the models effectively while adhering to ethical considerations. Additionally, exploring the community forums and resources can help you gain insights and best practices for leveraging Anthropic's 
# technologies.",
#     additional_kwargs={'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 112,
#             'prompt_tokens': 47,
#             'total_tokens': 159,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-mini-2024-07-18',
#         'system_fingerprint': 'fp_0aa8d3e20b',
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-70f207ac-e821-4f44-8169-bcf1a5703786-0',
#     usage_metadata={'input_tokens': 47, 'output_tokens': 112, 'total_tokens': 159, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )

print(' ')
results = full_chain.invoke({"question": "how do I use LangChain?"})
rprint(results)
# AIMessage(
#     content='As Harrison Chase told me, to use LangChain, you should start by understanding its core components, which include chains, agents, and memory. Begin by installing the LangChain library via pip, and then explore the
# various modules it offers for different functionalities such as LLMs (Large Language Models), document loaders, and prompt templates. \n\nYou can create a simple chain by defining a sequence of tasks that process input data, 
# and you can utilize agents to make decisions based on user queries. Additionally, incorporating memory allows your application to maintain context over interactions. \n\nTo get started, consider following the official 
# documentation for step-by-step guides, examples, and best practices. Experimenting with sample projects will also help you grasp how to integrate LangChain into your applications effectively.',
#     additional_kwargs={'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 154,
#             'prompt_tokens': 44,
#             'total_tokens': 198,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-mini-2024-07-18',
#         'system_fingerprint': 'fp_d02d531b47',
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-cc122c9a-6a59-4e94-96b8-cf3b00790f61-0',
#     usage_metadata={'input_tokens': 44, 'output_tokens': 154, 'total_tokens': 198, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )

print(' ')
results = full_chain.invoke({"question": "whats 2 + 2"})
rprint(results)
# AIMessage(
#     content='2 + 2 equals 4.',
#     additional_kwargs={'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 9,
#             'prompt_tokens': 24,
#             'total_tokens': 33,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-mini-2024-07-18',
#         'system_fingerprint': 'fp_0aa8d3e20b',
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-d3884d73-dc7f-4a7e-8a96-cf418f5f5fb8-0',
#     usage_metadata={'input_tokens': 24, 'output_tokens': 9, 'total_tokens': 33, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )


##################################################################################
### 2. RunnableBranch로 라우팅 하기
### RunnableBranch는 입력을 기반으로 실행할 조건과 runnable 세트를 정의할 수 있는 특별한 유형의 runnable
print('2.', '-' * 50)
##################################################################################
from langchain_core.runnables import RunnableBranch

branch = RunnableBranch(
    (lambda x: "anthropic" in x["topic"].lower(), anthropic_chain),
    (lambda x: "langchain" in x["topic"].lower(), langchain_chain),
    general_chain,
)
full_chain = {"topic": chain, "question": lambda x: x["question"]} | branch

results = full_chain.invoke({"question": "how do I use Anthropic?"})
rprint(results)
# 2. --------------------------------------------------
# AIMessage(
#     content="As Dario Amodei told me, using Anthropic involves understanding its various AI products and their applications. You can start by exploring the API or platform that Anthropic offers, which allows you to integrate 
# their language models into your applications. It's important to familiarize yourself with the documentation provided, as it outlines how to make requests, handle responses, and implement best practices for safety and 
# alignment. Additionally, consider experimenting with different prompts and settings to see how the model behaves in various contexts, and always keep in mind the ethical implications of using AI technologies.",
#     additional_kwargs={'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 111,
#             'prompt_tokens': 47,
#             'total_tokens': 158,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-mini-2024-07-18',
#         'system_fingerprint': 'fp_d02d531b47',
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-ff53996b-030d-4642-a2df-364bbf5989bb-0',
#     usage_metadata={'input_tokens': 47, 'output_tokens': 111, 'total_tokens': 158, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )

print(' ')
results = full_chain.invoke({"question": "how do I use LangChain?"})
rprint(results)
# AIMessage(
#     content='As Harrison Chase told me, to use LangChain, you should start by installing the library via pip. You can do this by running `pip install langchain`. Once installed, you can import the necessary modules and begin 
# to construct your language model applications. \n\nLangChain provides a framework for chaining together different components like language models, data loaders, and processing pipelines. You can create chains of operations 
# that allow you to define how data flows through your application. \n\nTo get started, you might want to explore the documentation and tutorials available on the LangChain website to understand the various components and how to
# integrate them effectively. Additionally, consider experimenting with example projects to see how you can utilize LangChain for specific tasks such as text generation, question answering, or document retrieval. \n\nRemember to
# keep an eye on the community and GitHub repository for updates and support as you develop your projects!',
#     additional_kwargs={'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 177,
#             'prompt_tokens': 44,
#             'total_tokens': 221,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-mini-2024-07-18',
#         'system_fingerprint': 'fp_0aa8d3e20b',
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-0a56c994-ec3b-49c2-b59e-982e717a3b72-0',
#     usage_metadata={'input_tokens': 44, 'output_tokens': 177, 'total_tokens': 221, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )

print(' ')
results = full_chain.invoke({"question": "whats 2 + 2"})
rprint(results)
# AIMessage(
#     content='2 + 2 equals 4.',
#     additional_kwargs={'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 9,
#             'prompt_tokens': 24,
#             'total_tokens': 33,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-mini-2024-07-18',
#         'system_fingerprint': 'fp_d02d531b47',
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-2829be07-3634-4410-a499-06cbc8181cfd-0',
#     usage_metadata={'input_tokens': 24, 'output_tokens': 9, 'total_tokens': 33, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )


##################################################################################
### 3. semantic similarity로 라우팅 하기
print('3.', '-' * 50)
##################################################################################
from langchain_community.utils.math import cosine_similarity
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import OpenAIEmbeddings

physics_template = """You are a very smart physics professor. \
You are great at answering questions about physics in a concise and easy to understand manner. \
When you don't know the answer to a question you admit that you don't know.

Here is a question:
{query}"""

math_template = """You are a very good mathematician. You are great at answering math questions. \
You are so good because you are able to break down hard problems into their component parts, \
answer the component parts, and then put them together to answer the broader question.

Here is a question:
{query}"""

embeddings = OpenAIEmbeddings()
prompt_templates = [physics_template, math_template]
prompt_embeddings = embeddings.embed_documents(prompt_templates)


def prompt_router(input):
    query_embedding = embeddings.embed_query(input["query"])
    similarity = cosine_similarity([query_embedding], prompt_embeddings)[0]
    most_similar = prompt_templates[similarity.argmax()]
    print("Using MATH" if most_similar == math_template else "Using PHYSICS")
    return PromptTemplate.from_template(most_similar)


chain = (
    {"query": RunnablePassthrough()}
    | RunnableLambda(prompt_router)
    | ChatOpenAI(model="gpt-4o-mini")
    | StrOutputParser()
)

rprint(chain.invoke("What's a black hole"))
# 3. --------------------------------------------------
# Using PHYSICS
# A black hole is an astronomical object with a gravitational pull so strong that nothing, not even light, can escape from it. This occurs when a massive star exhausts its nuclear fuel and collapses under its own gravity, 
# compressing its mass into a very small volume. The boundary surrounding a black hole is called the event horizon; once something crosses this boundary, it cannot return. Black holes can vary in size, from stellar black holes 
# formed by the collapse of individual stars to supermassive black holes that reside at the centers of galaxies and contain millions to billions of times the mass of the Sun.

print(' ')
rprint(chain.invoke("What's a path integral"))
# Using MATH
# A path integral is a concept primarily used in physics and mathematics, particularly in the context of quantum mechanics and field theory. It provides a way to calculate the probability amplitudes of different paths that a 
# particle can take between two points in space and time. Here’s a breakdown of the concept:

# ### Component Parts:
# ...