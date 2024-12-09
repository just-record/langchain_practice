from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import DatetimeOutputParser


prompt = ChatPromptTemplate.from_template(
    "what time was {event} (in %Y-%m-%dT%H:%M:%S.%fZ format - only return this value)"
)

# In this case we are going to do the fallbacks on the LLM + output parser level
# Because the error will get raised in the OutputParser
openai_35 = ChatOpenAI(model="gpt-3.5-turbo") | DatetimeOutputParser()
openai_4o = ChatOpenAI(model="gpt-4o") | DatetimeOutputParser()

only_35 = prompt | openai_35
fallback_4o = prompt | openai_35.with_fallbacks([openai_4o])


### 1. gpt-3.5-turbo(조금 어려운 기능)
try:
    print(only_35.invoke({"event": "the superbowl in 1994"}))
except Exception as e:
    print(f"Error: {e}")
# 출력: gpt-3.5-turbo도 성능이 좋아 져서 오류가 발생하지 않음. 아래는 공식 문서에서 발생하는 오류
# Error: Could not parse datetime string: The Super Bowl in 1994 took place on January 30th at 3:30 PM local time. Converting this to the specified format (%Y-%m-%dT%H:%M:%S.%fZ) results in: 1994-01-30T15:30:00.000Z

print('-'*30)

### 2. fallbacks을 사용하여 좋은 모델로 요청
try:
    print(fallback_4o.invoke({"event": "the superbowl in 1994"}))
except Exception as e:
    print(f"Error: {e}")
# 출력
# 1994-01-30 18:30:00
