from dotenv import load_dotenv
load_dotenv()

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain import hub
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor

# Tools - 'Tavily'
search = TavilySearchResults(max_results=2)

# Tools - 'Retriever'
loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
docs = loader.load()
documents = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200
).split_documents(docs)
vector = FAISS.from_documents(documents, OpenAIEmbeddings())
retriever = vector.as_retriever()
retriever_tool = create_retriever_tool(
    retriever,
    "langsmith_search",
    "Search for information about LangSmith. For any questions about LangSmith, you must use this tool!",
)

tools = [search, retriever_tool]

# model with tools
model = ChatOpenAI(model="gpt-4o")
model_with_tools = model.bind_tools(tools)

# agent
prompt = hub.pull("hwchase17/openai-functions-agent")
# [SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], template='You are a helpful assistant')), MessagesPlaceholder(variable_name='chat_history', optional=True), HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['input'], template='{input}')), MessagesPlaceholder(variable_name='agent_scratchpad')]

agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

### 1. 메모리에 추가 하기 - 'chat_history' 사용 하여 이전 대화 기억 하기
# A. 첫 번째 대화 - 이름 말하기
# Here we pass in an empty list of messages for chat_history because it is the first message in the chat
print(agent_executor.invoke({"input": "hi! my name is bob", "chat_history": []}))
# {'input': 'hi! my name is bob', 'chat_history': [], 'output': 'Hello, Bob! How can I assist you today?'}

# B. 두 번째 대화 - 이름 묻기 - 'chat_history'에 이전 대화 추가
print('-'*30)
from langchain_core.messages import AIMessage, HumanMessage
print(agent_executor.invoke(
    {
        "chat_history": [
            HumanMessage(content="hi! my name is bob"),
            AIMessage(content="Hello Bob! How can I assist you today?"),
        ],
        "input": "what's my name?",
    }
))
# {'chat_history': [HumanMessage(content='hi! my name is bob'), AIMessage(content='Hello Bob! How can I assist you today?')], 'input': "what's my name?", 'output': 'Your name is Bob. How can I assist you further?'}


### 2. 자동으로 이전 대화 기억 하기
print('-'*30)
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

# C-1. 이름 말하기
print(agent_with_chat_history.invoke(
    {"input": "hi! I'm bob"},
    config={"configurable": {"session_id": "<foo>"}},
))
# {'input': "hi! I'm bob", 'chat_history': [], 'output': 'Hello, Bob! How can I assist you today?'}

# C-2. 이름 묻기
print('-'*30)
print(agent_with_chat_history.invoke(
    {"input": "what's my name?"},
    config={"configurable": {"session_id": "<foo>"}},
))
# {'input': "what's my name?", 'chat_history': [HumanMessage(content="hi! I'm bob"), AIMessage(content='Hello Bob! How can I assist you today?')], 'output': 'You mentioned that your name is Bob. How can I help you today, Bob?'}