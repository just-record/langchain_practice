from dotenv import load_dotenv
load_dotenv()

import openai
from langsmith.wrappers import wrap_openai
from langsmith import traceable

### 1. 추적 로깅
# Auto-trace LLM calls in-context
client = wrap_openai(openai.Client())

@traceable # Auto-trace this function
def pipeline(user_input: str):
    result = client.chat.completions.create(
        messages=[{"role": "user", "content": user_input}],
        model="gpt-3.5-turbo"
    )
    return result.choices[0].message.content

print(pipeline("Hello, world!"))
# Hello! How may I assist you today?

# - LangSmith 사이트 로그인
# - 'Projects' -> 'LANGCHAIN_PRACTICE' -> 'pipeline' -> TRACE 확인
#   - 'pipeline': Input - 'user_input: Hello, world!', Output - 'Hello! How may I assist you today?'
#   - 'ChatOpenAI', 'gpt-3.5-turbo': Input - 'Hello, world!', Output - 'Hello! How may I assist you today?'


### 2. 평가 하기
# 우선 이런게 있다는 것 정도만 알아두기
print('-'*30)
from langsmith import Client
from langsmith.evaluation import evaluate

client = Client()

# Define dataset: these are your test cases
dataset_name = "Sample Dataset"
dataset = client.create_dataset(dataset_name, description="A sample dataset in LangSmith.")
client.create_examples(
    inputs=[
        {"postfix": "to LangSmith"},
        {"postfix": "to Evaluations in LangSmith"},
    ],
    outputs=[
        {"output": "Welcome to LangSmith"},
        {"output": "Welcome to Evaluations in LangSmith"},
    ],
    dataset_id=dataset.id,
)

# Define your evaluator
def exact_match(run, example):
    return {"score": run.outputs["output"] == example.outputs["output"]}

experiment_results = evaluate(
    lambda input: "Welcome " + input['postfix'], # Your AI system goes here
    data=dataset_name, # The data to predict and grade over
    evaluators=[exact_match], # The evaluators to score the results
    experiment_prefix="sample-experiment", # The name of the experiment
    metadata={
      "version": "1.0.0",
      "revision_id": "beta"
    },
)

# print(experiment_results)
