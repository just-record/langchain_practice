# Conversation Retrieval Chain - 1

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains import create_retrieval_chain
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
docs = loader.load()
embeddings = OpenAIEmbeddings()
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = FAISS.from_documents(documents, embeddings)

prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
])


llm = ChatOpenAI()

# output_parser = StrOutputParser()

# document_chain = create_stuff_documents_chain(llm, prompt)


retriever = vector.as_retriever()
retriever_chain = create_history_aware_retriever(llm, retriever, prompt)
# retrieval_chain = create_retrieval_chain(retriever, document_chain)

chat_history = [HumanMessage(content="Can LangSmith help test my LLM applications?"), AIMessage(content="Yes!")]
response = retriever_chain.invoke({
    "chat_history": chat_history,
    "input": "Tell me how"
})

# response = retriever_chain.invoke({"input": "how can langsmith help with testing?"})
print(response['answer'])