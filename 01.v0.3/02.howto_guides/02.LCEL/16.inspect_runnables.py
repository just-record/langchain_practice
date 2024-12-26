from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

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

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)


##################################################################################
### 1. Get a graph, Print the graph
print('1.', '-' * 50)
##################################################################################
chain.get_graph()

chain.get_graph().print_ascii()
# 1. --------------------------------------------------
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


##################################################################################
### 2. Get the prompts
print('2.', '-' * 50)
##################################################################################
rprint(chain.get_prompts())
# 2. --------------------------------------------------
# [
#     ChatPromptTemplate(
#         input_variables=['context', 'question'],
#         input_types={},
#         partial_variables={},
#         messages=[
#             HumanMessagePromptTemplate(
#                 prompt=PromptTemplate(input_variables=['context', 'question'], input_types={}, partial_variables={}, template='Answer the question based only on the following context:\n{context}\n\nQuestion: {question}\n'),
#                 additional_kwargs={}
#             )
#         ]
#     )
# ]