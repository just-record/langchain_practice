# Serving with LangServe - Client

# 잘 모르겠다.

from langserve import RemoteRunnable
from langchain_core.messages import HumanMessage, AIMessage

chat_history = [HumanMessage(content="Can LangSmith help test my LLM applications?"), AIMessage(content="Yes!")]

remote_chain = RemoteRunnable("http://localhost:8000/agent/")
# remote_chain.invoke({"input": "how can langsmith help with testing?"})
remote_chain.invoke({
    "chat_history": chat_history,
    "input": "Tell me how"
})



