from dotenv import load_dotenv
load_dotenv()

### Tool: 'Tavily' - API Key 필요, 'Retriever'
from langchain_community.tools.tavily_search import TavilySearchResults

### 1. 'Tavily'
search = TavilySearchResults(max_results=2)
print(search.invoke("what is the weather in SF"))
# [{'url': 'https://www.weatherapi.com/', 'content': "{'location': {'name': 'San Francisco', 'region': 'California', 'country': 'United States of America', 'lat': 37.78, 'lon': -122.42, 'tz_id': 'America/Los_Angeles', 'localtime_epoch': 1720590176, 'localtime': '2024-07-09 22:42'}, 'current': {'last_updated_epoch': 1720589400, 'last_updated': '2024-07-09 22:30', 'temp_c': 16.1, 'temp_f': 61.0, 'is_day': 0, 'condition': {'text': 'Overcast', 'icon': '//cdn.weatherapi.com/weather/64x64/night/122.png', 'code': 1009}, 'wind_mph': 11.9, 'wind_kph': 19.1, 'wind_degree': 300, 'wind_dir': 'WNW', 'pressure_mb': 1013.0, 'pressure_in': 29.9, 'precip_mm': 0.0, 'precip_in': 0.0, 'humidity': 93, 'cloud': 100, 'feelslike_c': 16.1, 'feelslike_f': 61.0, 'windchill_c': 13.8, 'windchill_f': 56.9, 'heatindex_c': 14.6, 'heatindex_f': 58.3, 'dewpoint_c': 13.0, 'dewpoint_f': 55.3, 'vis_km': 16.0, 'vis_miles': 9.0, 'uv': 1.0, 'gust_mph': 13.6, 'gust_kph': 21.9}}"}, {'url': 'https://www.wunderground.com/hourly/us/ca/san-francisco/94188/date/2024-7-10', 'content': 'San Francisco Weather Forecasts. Weather Underground provides local & long-range weather forecasts, weatherreports, maps & tropical weather conditions for the San Francisco area. ... Wednesday 07/ ...'}]


### 2. 'Retriever'
print('-'*30)
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool

loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
docs = loader.load()
documents = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200
).split_documents(docs)
vector = FAISS.from_documents(documents, OpenAIEmbeddings())
retriever = vector.as_retriever()

print(retriever.invoke("how to upload a dataset")[0])
# page_content='description="A sample dataset in LangSmith.")client.create_examples(    inputs=[        {"postfix": "to LangSmith"},        {"postfix": "to Evaluations in LangSmith"},    ],    outputs=[        {"output": "Welcome to LangSmith"},        {"output": "Welcome to Evaluations in LangSmith"},    ],    dataset_id=dataset.id,)# Define your evaluatordef exact_match(run, example):    return {"score": run.outputs["output"] == example.outputs["output"]}experiment_results = evaluate(    lambda input: "Welcome " + input[\'postfix\'], # Your AI system goes here    data=dataset_name, # The data to predict and grade over    evaluators=[exact_match], # The evaluators to score the results    experiment_prefix="sample-experiment", # The name of the experiment    metadata={      "version": "1.0.0",      "revision_id": "beta"    },)import { Client, Run, Example } from "langsmith";import { evaluate } from "langsmith/evaluation";import { EvaluationResult } from "langsmith/evaluation";const client = new' metadata={'source': 'https://docs.smith.langchain.com/overview', 'title': 'Get started with LangSmith | 🦜️🛠️ LangSmith', 'description': 'LangSmith is a platform for building production-grade LLM applications. It allows you to closely monitor and evaluate your application, so you can ship quickly and with confidence. Use of LangChain is not necessary - LangSmith works on its own!', 'language': 'en'}

retriever_tool = create_retriever_tool(
    retriever,
    "langsmith_search",
    "Search for information about LangSmith. For any questions about LangSmith, you must use this tool!",
)

tools = [search, retriever_tool]


### 3. model
print('-'*30)
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


model = ChatOpenAI(model="gpt-4o")

response = model.invoke([HumanMessage(content="hi!")])
print(response.content)
# Hello! How can I assist you today?


### 4. model with tools
print('-'*30)
model_with_tools = model.bind_tools(tools)

# 일반 질의
response = model_with_tools.invoke([HumanMessage(content="Hi!")])

print(f"ContentString: {response.content}")
# ContentString: Hello! How can I assist you today?
print(f"ToolCalls: {response.tool_calls}")
# ToolCalls: []

# 도구 호출이 필요 한 질의
print('-'*30)
response = model_with_tools.invoke([HumanMessage(content="What's the weather in SF?")])

print(f"ContentString: {response.content}")
# ContentString: 
print(f"ToolCalls: {response.tool_calls}")
# ToolCalls: [{'name': 'tavily_search_results_json', 'args': {'query': 'current weather in San Francisco'}, 'id': 'call_nKwa7vNUIJfj9lJaa7BiFCNj'}]

### 5. agent 생성
print('-'*30)
from langchain import hub
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor

# Get the prompt to use - you can modify this!
prompt = hub.pull("hwchase17/openai-functions-agent")
print(prompt.messages)
# [SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], template='You are a helpful assistant')), MessagesPlaceholder(variable_name='chat_history', optional=True), HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['input'], template='{input}')), MessagesPlaceholder(variable_name='agent_scratchpad')]

agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)


### 6. agent 실행
print('-'*30)
# A. 일반 질의
print(agent_executor.invoke({"input": "hi!"}))
# {'input': 'hi!', 'output': 'Hello! How can I assist you today?'}

# B. 'Retriever' 도구 호출이 필요한 질의
print('-'*30)
print(agent_executor.invoke({"input": "how can langsmith help with testing?"}))
# {'input': 'how can langsmith help with testing?', 'output': 'LangSmith offers several features that can significantly aid in the testing of AI applications, particularly those involving large language models (LLMs). Here are some ways LangSmith can help with testing:\n\n1. **Logging Traces**:\n   - LangSmith enables you to log traces of your application\'s execution. This helps in understanding how your application processes data and where it might be going wrong.\n   - You can log traces using their SDKs available for Python and TypeScript.\n\n2. **Creating Datasets for Testing**:\n   - LangSmith allows you to create datasets that can be used as test cases. These datasets can include various input-output pairs that your application should be able to handle correctly.\n   - You can create these datasets programmatically using the LangSmith client.\n\n3. **Evaluation Metrics**:\n   - LangSmith provides built-in evaluators to measure the correctness of the responses generated by your LLM. These evaluators can be either built-in or custom-defined.\n   - You can run evaluations on datasets to check how well your model is performing against expected outputs.\n\n4. **Custom Evaluators**:\n   - You can define custom evaluation criteria to suit specific needs of your application. This can include metrics like exact match, contextual accuracy, or any other custom metric that you define.\n\n5. **Integration with LangChain**:\n   - While LangSmith can operate independently, it also integrates well with LangChain, enabling you to use various tools and LLMs required for more comprehensive testing.\n\n6. **API for Automation**:\n   - LangSmith provides an API that allows you to automate the testing process. This can be particularly useful for continuous integration and deployment (CI/CD) pipelines.\n\n7. **User Interface**:\n   - The LangSmith UI provides a visual representation of your datasets, evaluations, and logs. This helps in quickly identifying issues and understanding the performance of your application.\n\n### Example Workflow\n\n1. **Install LangSmith SDK**:\n   ```bash\n   pip install -U langsmith\n   ```\n\n2. **Set Up Environment**:\n   ```bash\n   export LANGCHAIN_TRACING_V2=true\n   export LANGCHAIN_API_KEY=<your-api-key>\n   ```\n\n3. **Log a Trace**:\n   ```python\n   from langsmith import Client\n   client = new Client()\n   ```\n\n4. **Create Dataset and Examples**:\n   ```python\n   dataset = client.createDataset("Sample Dataset", description="A sample dataset in LangSmith.")\n   client.createExamples(\n       inputs=[{"postfix": "to LangSmith"}, {"postfix": "to Evaluations in LangSmith"}],\n       outputs=[{"output": "Welcome to LangSmith"}, {"output": "Welcome to Evaluations in LangSmith"}],\n       datasetId=dataset.id\n   )\n   ```\n\n5. **Run Evaluation**:\n   ```python\n   from langsmith.evaluation import evaluate, EvaluationResult\n   async def exactMatch(run, example):\n       return EvaluationResult(key="exact_match", score=run.outputs[\'output\'] == example.outputs[\'output\'])\n   \n   evaluate(lambda input: {"output": f"Welcome {input[\'postfix\']}"}, data="Sample Dataset", evaluators=[exactMatch])\n   ```\n\nBy following these steps, you can set up a robust testing framework for your LLM applications using LangSmith.'}

# C. 'Tavily' 도구 호출이 필요한 질의
print('-'*30)
print(agent_executor.invoke({"input": "whats the weather in sf?"}))
# {'input': 'whats the weather in sf?', 'output': 'The current weather in San Francisco is overcast with a temperature of 61°F (16.1°C). The wind is coming from the west-northwest at 11.9 mph (19.1 kph), and the humidity is at 93%. The visibility is 9 miles (16 km), and the UV index is 1.'}
