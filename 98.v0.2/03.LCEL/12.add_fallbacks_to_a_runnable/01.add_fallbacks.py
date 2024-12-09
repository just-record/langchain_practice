from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

# Note that we set max_retries = 0 to avoid retrying on RateLimits, etc
openai_llm_gptfake = ChatOpenAI(model="gpt-fake", max_retries=0)
openai_llm_gpt35 = ChatOpenAI(model="gpt-3.5-turbo")
llm = openai_llm_gptfake.with_fallbacks([openai_llm_gpt35])

### 1. 오류 발생 모델 호출
try:
    print(openai_llm_gptfake.invoke("Why did the chicken cross the road?"))
except Exception as e:
    print(f'Error: {e}')
# 출력
# Error: Error code: 404 - {'error': {'message': 'The model `gpt-fake` does not exist or you do not have access to it.', 'type': 'invalid_request_error', 'param': None, 'code': 'model_not_found'}}    

print('-'*30)

### 2. Fallbacks를 사용한 오류 발생 모델 호출
try:
    print(llm.invoke("Why did the chicken cross the road?"))
except Exception as e:
    print(f'Error: {e}')
# 출력
# content='To get to the other side.' response_metadata={'token_usage': {'completion_tokens': 7, 'prompt_tokens': 15, 'total_tokens': 22}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-8f4e6c34-3120-452f-b655-cf1e39670cfa-0' usage_metadata={'input_tokens': 15, 'output_tokens': 7, 'total_tokens': 22}