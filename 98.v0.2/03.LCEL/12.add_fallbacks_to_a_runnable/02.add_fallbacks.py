from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Note that we set max_retries = 0 to avoid retrying on RateLimits, etc
openai_llm_gptfake = ChatOpenAI(model="gpt-fake", max_retries=0)
openai_llm_gpt35 = ChatOpenAI(model="gpt-3.5-turbo")
llm = openai_llm_gptfake.with_fallbacks([openai_llm_gpt35])

chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You're a nice assistant who always includes a compliment in your response",
        ),
        ("human", "Why did the {animal} cross the road"),
    ]
)

chain = chat_prompt | llm

### 보통의 chain에 fallbacks을 적용
try:
    print(chain.invoke("Why did the chicken cross the road?"))
except Exception as e:
    print(f'Error: {e}')
# 출력
# content="That's a classic joke! You have a great sense of humor." response_metadata={'token_usage': {'completion_tokens': 14, 'prompt_tokens': 38, 'total_tokens': 52}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-f4fc0b1f-4683-4d1f-b15a-e2b7331a8286-0' usage_metadata={'input_tokens': 38, 'output_tokens': 14, 'total_tokens': 52}
