from langchain_core.runnables import RunnableLambda, RunnableParallel

runnable1 = RunnableLambda(lambda x: {"foo": x})
runnable2 = RunnableLambda(lambda x: [x] * 2)
runnable3 = RunnableLambda(lambda x: str(x))

chain = runnable1 | RunnableParallel(second=runnable2, third=runnable3)

chain.get_graph().print_ascii()
#                              +-------------+                              
#                              | LambdaInput |                              
#                              +-------------+                              
#                                     *                                     
#                                     *                                     
#                                     *                                     
#                     +------------------------------+                      
#                     | Lambda(lambda x: {'foo': x}) |                      
#                     +------------------------------+                      
#                                     *                                     
#                                     *                                     
#                                     *                                     
#                      +-----------------------------+                      
#                      | Parallel<second,third>Input |                      
#                      +-----------------------------+                      
#                         ****                  ***                         
#                     ****                         ****                     
#                   **                                 **                   
# +---------------------------+               +--------------------------+  
# | Lambda(lambda x: [x] * 2) |               | Lambda(lambda x: str(x)) |  
# +---------------------------+               +--------------------------+  
#                         ****                  ***                         
#                             ****          ****                            
#                                 **      **                                
#                     +------------------------------+                      
#                     | Parallel<second,third>Output |                      
#                     +------------------------------+   