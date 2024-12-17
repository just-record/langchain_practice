from langchain_core.runnables import RunnableLambda, RunnableParallel
from rich import print as rprint

runnable1 = RunnableLambda(lambda x: {"foo": x})
runnable2 = RunnableLambda(lambda x: [x] * 2)
runnable3 = RunnableLambda(lambda x: str(x))

chain = runnable1 | RunnableParallel(second=runnable2, third=runnable3)

##################################################################################
### 1. Runnable 객체들의 실행 흐름을 시각적으로 표현하는 방법
### .get_graph()를 사용하여 실행 흐름을 그래프로 출력
print('1.', '-' * 50)
##################################################################################
chain.get_graph().print_ascii()
#         +-------------+          
#         | LambdaInput |          
#         +-------------+          
#                 *                
#                 *                
#                 *                
#            +--------+            
#            | Lambda |            
#            +--------+            
#                 *                
#                 *                
#                 *                
# +-----------------------------+  
# | Parallel<second,third>Input |  
# +-----------------------------+  
#            *         *           
#          **           **         
#         *               *        
#  +--------+          +--------+  
#  | Lambda |          | Lambda |  
#  +--------+          +--------+  
#            *         *           
#             **     **            
#               *   *              
# +------------------------------+ 
# | Parallel<second,third>Output | 
# +------------------------------+ 


##################################################################################
### 2. print_ascii() 제외
print('2.', '-' * 50)
##################################################################################
print(type(chain.get_graph()))
# 2. --------------------------------------------------
# <class 'langchain_core.runnables.graph.Graph'>

print(' ')
rprint(chain.get_graph())
# Graph(
#     nodes={
#         '3b7811c6a5614d5b87b0ef99e06892dc': Node(id='3b7811c6a5614d5b87b0ef99e06892dc', name='LambdaInput', data=<class 'langchain_core.runnables.base.RunnableLambdaInput'>, metadata=None),
#         '50519f5f55cb4b209cfa6a79082458e8': Node(id='50519f5f55cb4b209cfa6a79082458e8', name='Lambda', data=RunnableLambda(lambda x: {'foo': x}), metadata=None),
#         '9840ed2ba3a24f3f9eb463261c957939': Node(
#             id='9840ed2ba3a24f3f9eb463261c957939',
#             name='Parallel<second,third>Input',
#             data=<class 'langchain_core.utils.pydantic.RunnableParallel<second,third>Input'>,
#             metadata=None
#         ),
#         'e8f47c4d994c4236be59ac025a9f6706': Node(
#             id='e8f47c4d994c4236be59ac025a9f6706',
#             name='Parallel<second,third>Output',
#             data=<class 'langchain_core.utils.pydantic.RunnableParallel<second,third>Output'>,
#             metadata=None
#         ),
#         '5016f9ab68b64c368c1b79f84d8bb000': Node(id='5016f9ab68b64c368c1b79f84d8bb000', name='Lambda', data=RunnableLambda(lambda x: [x] * 2), metadata=None),
#         '5c42c20d853042ecb7165218c9666994': Node(id='5c42c20d853042ecb7165218c9666994', name='Lambda', data=RunnableLambda(lambda x: str(x)), metadata=None)
#     },
#     edges=[
#         Edge(source='3b7811c6a5614d5b87b0ef99e06892dc', target='50519f5f55cb4b209cfa6a79082458e8', data=None, conditional=False),
#         Edge(source='9840ed2ba3a24f3f9eb463261c957939', target='5016f9ab68b64c368c1b79f84d8bb000', data=None, conditional=False),
#         Edge(source='5016f9ab68b64c368c1b79f84d8bb000', target='e8f47c4d994c4236be59ac025a9f6706', data=None, conditional=False),
#         Edge(source='9840ed2ba3a24f3f9eb463261c957939', target='5c42c20d853042ecb7165218c9666994', data=None, conditional=False),
#         Edge(source='5c42c20d853042ecb7165218c9666994', target='e8f47c4d994c4236be59ac025a9f6706', data=None, conditional=False),
#         Edge(source='50519f5f55cb4b209cfa6a79082458e8', target='9840ed2ba3a24f3f9eb463261c957939', data=None, conditional=False)
#     ]
# )