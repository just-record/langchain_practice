from dotenv import load_dotenv
load_dotenv()

from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


vectorstore = FAISS.from_texts(
    ["harrison worked at kensho"], embedding=OpenAIEmbeddings()
)

retriever = vectorstore.as_retriever()

template = """Answer the question based only on the following context:
{context}

Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

model = ChatOpenAI()

results = chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)
print(results)

### 1. Get a graph
chain.get_graph()
### 2. Print a graph
chain.get_graph().print_ascii()

### 3. Get the prompts
print(chain.get_prompts())


### 2. 출력
#            +---------------------------------+         
#            | Parallel<context,question>Input |         
#            +---------------------------------+         
#                     **               **                
#                  ***                   ***             
#                **                         **           
# +----------------------+              +-------------+  
# | VectorStoreRetriever |              | Passthrough |  
# +----------------------+              +-------------+  
#                     **               **                
#                       ***         ***                  
#                          **     **                     
#            +----------------------------------+        
#            | Parallel<context,question>Output |        
#            +----------------------------------+        
#                              *                         
#                              *                         
#                              *                         
#                   +--------------------+               
#                   | ChatPromptTemplate |               
#                   +--------------------+               
#                              *                         
#                              *                         
#                              *                         
#                       +------------+                   
#                       | ChatOpenAI |                   
#                       +------------+                   
#                              *                         
#                              *                         
#                              *                         
#                    +-----------------+                 
#                    | StrOutputParser |                 
#                    +-----------------+                 
#                              *                         
#                              *                         
#                              *                         
#                 +-----------------------+              
#                 | StrOutputParserOutput |              
#                 +-----------------------+  