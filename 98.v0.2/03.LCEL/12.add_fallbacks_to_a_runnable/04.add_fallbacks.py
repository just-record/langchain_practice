from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI


short_llm = ChatOpenAI(model="gpt-3.5-turbo")
long_llm = ChatOpenAI(model="gpt-4o")
llm = short_llm.with_fallbacks([long_llm])

# inputs = "What is the next number: " + ", ".join(["one", "two"] * 3000)
inputs = "What is the next number: " + ", ".join([str(i) for i in range(5000)])
print(f'inputs length: {len(inputs)}')


### 1. 입력이 작은 모델에 큰 입력 전달
try:
    print(short_llm.invoke(inputs))
except Exception as e:
    print(f'Error: {e}')
# 출력: Error
# Error: Error code: 400 - {'error': {'message': "This model's maximum context length is 16385 tokens. ...

print('-'*30)

### 2. fallbacks을 사용하여 큰 모델에 큰 입력 전달
try:
    print(llm.invoke(inputs))
except Exception as e:
    print(f'Error: {e}')
# 출력: 5000
# content='The next number in the sequence is 5000 ...
