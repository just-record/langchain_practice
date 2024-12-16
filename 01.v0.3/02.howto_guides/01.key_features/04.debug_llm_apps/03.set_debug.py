from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate


llm = ChatOpenAI(model="gpt-4o-mini")
tools = [TavilySearchResults(max_results=1)]
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant.",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_tool_calling_agent(llm, tools, prompt)


#################################################################################
### 1. set_debug
### 전역 디버그 플래그를 설정하면 콜백을 지원하는 모든 LangChain 컴포넌트(체인, 모델, 에이전트, 도구, 리트리버)가 받은 입력과 생성한 출력을 출력.
### 이는 가장 상세한 설정이며 원시 입력과 출력을 모두 기록합니다.
print('1.', '-' * 50)
##################################################################################
from langchain.globals import set_verbose
from langchain.globals import set_debug

set_debug(True)
set_verbose(False)
agent_executor = AgentExecutor(agent=agent, tools=tools)

results = agent_executor.invoke(
    {"input": "Who directed the 2023 film Oppenheimer and what is their age in days?"}
)
rprint(results)
# 1. --------------------------------------------------
# [chain/start] [chain:AgentExecutor] Entering Chain run with input:
# {
#   "input": "Who directed the 2023 film Oppenheimer and what is their age in days?"
# }
# [chain/start] [chain:AgentExecutor > chain:RunnableSequence] Entering Chain run with input:
# {
#   "input": ""
# }
# [chain/start] [chain:AgentExecutor > chain:RunnableSequence > chain:RunnableAssign<agent_scratchpad>] Entering Chain run with input:
# {
#   "input": ""
# }
# [chain/start] [chain:AgentExecutor > chain:RunnableSequence > chain:RunnableAssign<agent_scratchpad> > chain:RunnableParallel<agent_scratchpad>] Entering Chain run with input:
# {
#   "input": ""
# }
# [chain/start] [chain:AgentExecutor > chain:RunnableSequence > chain:RunnableAssign<agent_scratchpad> > chain:RunnableParallel<agent_scratchpad> > chain:RunnableLambda] Entering Chain run with input:
# {
#   "input": ""
# }
# [chain/end] [chain:AgentExecutor > chain:RunnableSequence > chain:RunnableAssign<agent_scratchpad> > chain:RunnableParallel<agent_scratchpad> > chain:RunnableLambda] [1ms] Exiting Chain run with output:
# {
#   "output": []
# }
# [chain/end] [chain:AgentExecutor > chain:RunnableSequence > chain:RunnableAssign<agent_scratchpad> > chain:RunnableParallel<agent_scratchpad>] [2ms] Exiting Chain run with output:
# {
#   "agent_scratchpad": []
# }
# [chain/end] [chain:AgentExecutor > chain:RunnableSequence > chain:RunnableAssign<agent_scratchpad>] [2ms] Exiting Chain run with output:
# {
#   "input": "Who directed the 2023 film Oppenheimer and what is their age in days?",
#   "intermediate_steps": [],
#   "agent_scratchpad": []
# }
# [chain/start] [chain:AgentExecutor > chain:RunnableSequence > prompt:ChatPromptTemplate] Entering Prompt run with input:
# {
#   "input": "Who directed the 2023 film Oppenheimer and what is their age in days?",
#   "intermediate_steps": [],
#   "agent_scratchpad": []
# }
# [chain/end] [chain:AgentExecutor > chain:RunnableSequence > prompt:ChatPromptTemplate] [0ms] Exiting Prompt run with output:
# [outputs]
# [llm/start] [chain:AgentExecutor > chain:RunnableSequence > llm:ChatOpenAI] Entering LLM run with input:
# {
#   "prompts": [
#     "System: You are a helpful assistant.\nHuman: Who directed the 2023 film Oppenheimer and what is their age in days?"
#   ]
# }
# [llm/end] [chain:AgentExecutor > chain:RunnableSequence > llm:ChatOpenAI] [1.67s] Exiting LLM run with output:
# {
#   "generations": [
#     [
#       {
#         "text": "",
#         "generation_info": {
#           "finish_reason": "tool_calls",
#           "model_name": "gpt-4o-mini-2024-07-18",
#           "system_fingerprint": "fp_39a40c96a0"
#         },
#         "type": "ChatGenerationChunk",
#         "message": {
#           "lc": 1,
#           "type": "constructor",
#           "id": [
#             "langchain",
#             "schema",
#             "messages",
#             "AIMessageChunk"
#           ],
#           "kwargs": {
#             "content": "",
#             "additional_kwargs": {
#               "tool_calls": [
#                 {
#                   "index": 0,
#                   "id": "call_ix3NexcVY1R5GRDyPieWeBen",
#                   "function": {
#                     "arguments": "{\"query\": \"Oppenheimer 2023 film director\"}",
#                     "name": "tavily_search_results_json"
#                   },
#                   "type": "function"
#                 },
#                 {
#                   "index": 1,
#                   "id": "call_fui0dzrY4E4CIYIWhL79dlBV",
#                   "function": {
#                     "arguments": "{\"query\": \"Oppenheimer 2023 film release date\"}",
#                     "name": "tavily_search_results_json"
#                   },
#                   "type": "function"
#                 }
#               ]
#             },
#             "response_metadata": {
#               "finish_reason": "tool_calls",
#               "model_name": "gpt-4o-mini-2024-07-18",
#               "system_fingerprint": "fp_39a40c96a0"
#             },
#             "type": "AIMessageChunk",
#             "id": "run-f26439c7-9098-4edb-bfbe-c20497b1317c",
#             "tool_calls": [
#               {
#                 "name": "tavily_search_results_json",
#                 "args": {
#                   "query": "Oppenheimer 2023 film director"
#                 },
#                 "id": "call_ix3NexcVY1R5GRDyPieWeBen",
#                 "type": "tool_call"
#               },
#               {
#                 "name": "tavily_search_results_json",
#                 "args": {
#                   "query": "Oppenheimer 2023 film release date"
#                 },
#                 "id": "call_fui0dzrY4E4CIYIWhL79dlBV",
#                 "type": "tool_call"
#               }
#             ],
#             "tool_call_chunks": [
#               {
#                 "name": "tavily_search_results_json",
#                 "args": "{\"query\": \"Oppenheimer 2023 film director\"}",
#                 "id": "call_ix3NexcVY1R5GRDyPieWeBen",
#                 "index": 0,
#                 "type": "tool_call_chunk"
#               },
#               {
#                 "name": "tavily_search_results_json",
#                 "args": "{\"query\": \"Oppenheimer 2023 film release date\"}",
#                 "id": "call_fui0dzrY4E4CIYIWhL79dlBV",
#                 "index": 1,
#                 "type": "tool_call_chunk"
#               }
#             ],
#             "invalid_tool_calls": []
#           }
#         }
#       }
#     ]
#   ],
#   "llm_output": null,
#   "run": null,
#   "type": "LLMResult"
# }
# [chain/start] [chain:AgentExecutor > chain:RunnableSequence > parser:ToolsAgentOutputParser] Entering Parser run with input:
# [inputs]
# [chain/end] [chain:AgentExecutor > chain:RunnableSequence > parser:ToolsAgentOutputParser] [0ms] Exiting Parser run with output:
# [outputs]
# [chain/end] [chain:AgentExecutor > chain:RunnableSequence] [1.68s] Exiting Chain run with output:
# [outputs]
# [tool/start] [chain:AgentExecutor > tool:tavily_search_results_json] Entering Tool run with input:
# "{'query': 'Oppenheimer 2023 film director'}"
# [tool/end] [chain:AgentExecutor > tool:tavily_search_results_json] [3.05s] Exiting Tool run with output:
# "[{'url': 'https://www.imdb.com/title/tt15398776/fullcredits/', 'content': 'Oppenheimer (2023) cast and crew credits, including actors, actresses, directors, writers and more. Menu. ... director of photography: behind-the-scenes Jason Gary ... best boy grip ... film loader Luc Poullain ... aerial coordinator'}]"
# [tool/start] [chain:AgentExecutor > tool:tavily_search_results_json] Entering Tool run with input:
# "{'query': 'Oppenheimer 2023 film release date'}"
# [tool/end] [chain:AgentExecutor > tool:tavily_search_results_json] [3.26s] Exiting Tool run with output:
# "[{'url': 'https://www.rottentomatoes.com/m/oppenheimer_2023', 'content': "Genre:\nHistory,\nDrama,\nBiography\nOriginal Language:\nEnglish\nDirector:\nChristopher Nolan\nProducer:\nEmma Thomas,\nCharles Roven,\nChristopher Nolan\nWriter:\nChristopher Nolan\nRelease Date (Theaters):\nJul 21, 2023\nwide\nRelease Date (Streaming):\nNov 21, 2023\nBox Office (Gross USA):\n$328.1M\nRuntime:\n3h 0m\nDistributor:\nUniversal Pictures\nProduction Co:\nGadget Films,\nUniversal Pictures,\nSyncopy,\nAtlas Entertainment\nSound Mix:\nDatasat, Dolby Digital\nCast & Crew\nCillian Murphy\nJ. Robert Oppenheimer\nEmily Blunt\nKitty Oppenheimer\nRobert Downey Jr.\nLewis Strauss\nMatt Damon\nLeslie Groves Jr.\nRami Malek\nDavid Hill\nFlorence Pugh\nJean Tatlock\nBenny Safdie\nEdward Teller\nMichael Angarano\nRobert Serber\nJosh Hartnett\nErnest Lawrence\nKenneth Branagh\nNiels Bohr\nCasey Affleck\nBoris Pash\n Dane DeHaan\nKenneth Nichols\nDylan Arnold\nFrank Oppenheimer\nDavid Krumholtz\nIsidor Rabi\nAlden Ehrenreich\nSenate Aide\nMatthew Modine\nVannevar Bush\nJosh Peck\nKenneth Bainbridge\nGary Oldman\nHarry Truman\nJason Clarke\nJack Quaid\nChristopher Nolan\nDirector\nChristopher Nolan\nScreenwriter\nEmma Thomas\nProducer\nCharles Roven\nProducer\nChristopher Nolan\nProducer\nHoyte Van Hoytema\nCinematographer\nJennifer Lame\nFilm Editing\nLudwig Göransson\nOriginal Music\nNews & Interviews for Oppenheimer\nAwards Leaderboard: Top Movies of 2023\nOscar Nominations 2024: The Complete List of Nominees\nRotten Tomatoes Predicts the 2024 Oscar Nominations\nCritic Reviews for Oppenheimer\nAudience Reviews for Oppenheimer\nThere are no featured audience reviews for Oppenheimer at this time.\n Movies / TV\nCelebrity\nNo Results Found\nMovies in theaters\nMovies at home\nMore\nCertified fresh picks\nNew TV Tonight\nMost Popular TV on RT\nMore\nCertified fresh pick\nColumns\nGuides\n65 Movies That Celebrate Black Joy\n100 Best Free Movies on YouTube (February 2024)\n Hubs\nBlack Heritage\nGolden Tomato Awards: Best Movies & TV of 2023\nRT News\n10 Films About Black Music That Turn Household Names into Household Stories\nMr. & Mrs. Smith First Reviews: Donald Glover & Maya Erskine Shine in ‘Compelling’ Reboot, Critics Say\nOppenheimer\n2023, History/Drama, 3h 0m\nWhat to know\nCritics Consensus\nOppenheimer marks another engrossing achievement from Christopher Nolan that benefits from Murphy's tour-de-force performance and stunning visuals.\n Movie & TV guides\nPlay Daily Tomato Movie Trivia\nAwards Tour\nDiscover What to Watch\nRotten Tomatoes Podcasts\nJoin The Newsletter\nGet the freshest reviews, news, and more delivered right to your inbox!\n"}]"
# [chain/start] [chain:AgentExecutor > chain:RunnableSequence] Entering Chain run with input:
# {
#   "input": ""
# }
# [chain/start] [chain:AgentExecutor > chain:RunnableSequence > chain:RunnableAssign<agent_scratchpad>] Entering Chain run with input:
# {
#   "input": ""
# }
# [chain/start] [chain:AgentExecutor > chain:RunnableSequence > chain:RunnableAssign<agent_scratchpad> > chain:RunnableParallel<agent_scratchpad>] Entering Chain run with input:
# {
#   "input": ""
# }
# [chain/start] [chain:AgentExecutor > chain:RunnableSequence > chain:RunnableAssign<agent_scratchpad> > chain:RunnableParallel<agent_scratchpad> > chain:RunnableLambda] Entering Chain run with input:
# {
#   "input": ""
# }
# [chain/end] [chain:AgentExecutor > chain:RunnableSequence > chain:RunnableAssign<agent_scratchpad> > chain:RunnableParallel<agent_scratchpad> > chain:RunnableLambda] [4ms] Exiting Chain run with output:
# [outputs]
# [chain/end] [chain:AgentExecutor > chain:RunnableSequence > chain:RunnableAssign<agent_scratchpad> > chain:RunnableParallel<agent_scratchpad>] [7ms] Exiting Chain run with output:
# [outputs]
# [chain/end] [chain:AgentExecutor > chain:RunnableSequence > chain:RunnableAssign<agent_scratchpad>] [9ms] Exiting Chain run with output:
# [outputs]
# [chain/start] [chain:AgentExecutor > chain:RunnableSequence > prompt:ChatPromptTemplate] Entering Prompt run with input:
# [inputs]
# [chain/end] [chain:AgentExecutor > chain:RunnableSequence > prompt:ChatPromptTemplate] [3ms] Exiting Prompt run with output:
# [outputs]
# [llm/start] [chain:AgentExecutor > chain:RunnableSequence > llm:ChatOpenAI] Entering LLM run with input:
# {
#   "prompts": [
#     "System: You are a helpful assistant.\nHuman: Who directed the 2023 film Oppenheimer and what is their age in days?\nAI: \nTool: [{\"url\": \"https://www.imdb.com/title/tt15398776/fullcredits/\", \"content\": \"Oppenheimer (2023) cast and crew credits, including actors, actresses, directors, writers and more. Menu. ... director of photography: behind-the-scenes Jason Gary ... best boy grip ... film loader Luc Poullain ... aerial coordinator\"}]\nTool: [{\"url\": \"https://www.rottentomatoes.com/m/oppenheimer_2023\", \"content\": \"Genre:\\nHistory,\\nDrama,\\nBiography\\nOriginal Language:\\nEnglish\\nDirector:\\nChristopher Nolan\\nProducer:\\nEmma Thomas,\\nCharles Roven,\\nChristopher Nolan\\nWriter:\\nChristopher Nolan\\nRelease Date (Theaters):\\nJul 21, 2023\\nwide\\nRelease Date (Streaming):\\nNov 21, 2023\\nBox Office (Gross USA):\\n$328.1M\\nRuntime:\\n3h 0m\\nDistributor:\\nUniversal Pictures\\nProduction Co:\\nGadget Films,\\nUniversal Pictures,\\nSyncopy,\\nAtlas Entertainment\\nSound Mix:\\nDatasat, Dolby Digital\\nCast & Crew\\nCillian Murphy\\nJ. Robert Oppenheimer\\nEmily Blunt\\nKitty Oppenheimer\\nRobert Downey Jr.\\nLewis Strauss\\nMatt Damon\\nLeslie Groves Jr.\\nRami Malek\\nDavid Hill\\nFlorence Pugh\\nJean Tatlock\\nBenny Safdie\\nEdward Teller\\nMichael Angarano\\nRobert Serber\\nJosh Hartnett\\nErnest Lawrence\\nKenneth Branagh\\nNiels Bohr\\nCasey Affleck\\nBoris Pash\\n Dane DeHaan\\nKenneth Nichols\\nDylan Arnold\\nFrank Oppenheimer\\nDavid Krumholtz\\nIsidor Rabi\\nAlden Ehrenreich\\nSenate Aide\\nMatthew Modine\\nVannevar Bush\\nJosh Peck\\nKenneth Bainbridge\\nGary Oldman\\nHarry Truman\\nJason Clarke\\nJack Quaid\\nChristopher Nolan\\nDirector\\nChristopher Nolan\\nScreenwriter\\nEmma Thomas\\nProducer\\nCharles Roven\\nProducer\\nChristopher Nolan\\nProducer\\nHoyte Van Hoytema\\nCinematographer\\nJennifer Lame\\nFilm Editing\\nLudwig Göransson\\nOriginal Music\\nNews & Interviews for Oppenheimer\\nAwards Leaderboard: Top Movies of 2023\\nOscar Nominations 2024: The Complete List of Nominees\\nRotten Tomatoes Predicts the 2024 Oscar Nominations\\nCritic Reviews for Oppenheimer\\nAudience Reviews for Oppenheimer\\nThere are no featured audience reviews for Oppenheimer at this time.\\n Movies / TV\\nCelebrity\\nNo Results Found\\nMovies in theaters\\nMovies at home\\nMore\\nCertified fresh picks\\nNew TV Tonight\\nMost Popular TV on RT\\nMore\\nCertified fresh pick\\nColumns\\nGuides\\n65 Movies That Celebrate Black Joy\\n100 Best Free Movies on YouTube (February 2024)\\n Hubs\\nBlack Heritage\\nGolden Tomato Awards: Best Movies & TV of 2023\\nRT News\\n10 Films About Black Music That Turn Household Names into Household Stories\\nMr. & Mrs. Smith First Reviews: Donald Glover & Maya Erskine Shine in ‘Compelling’ Reboot, Critics Say\\nOppenheimer\\n2023, History/Drama, 3h 0m\\nWhat to know\\nCritics Consensus\\nOppenheimer marks another engrossing achievement from Christopher Nolan that benefits from Murphy's tour-de-force performance and stunning visuals.\\n Movie & TV guides\\nPlay Daily Tomato Movie Trivia\\nAwards Tour\\nDiscover What to Watch\\nRotten Tomatoes Podcasts\\nJoin The Newsletter\\nGet the freshest reviews, news, and more delivered right to your inbox!\\n\"}]"
#   ]
# }
# [llm/end] [chain:AgentExecutor > chain:RunnableSequence > llm:ChatOpenAI] [6.09s] Exiting LLM run with output:
# {
#   "generations": [
#     [
#       {
#         "text": "The 2023 film \"Oppenheimer\" was directed by Christopher Nolan. \n\nTo calculate Christopher Nolan's age in days, we need his birth date. Christopher Nolan was born on July 30, 1970. \n\nLet's calculate his age in days as of today, which is October 5, 2023.\n\n1. Calculate the total number of days from his birth date to today.\n2. From July 30, 1970, to July 30, 2023, is 53 years.\n3. From July 30, 2023, to October 5, 2023, is 2 months and 5 days.\n\nNow, let's break it down:\n\n- 53 years * 365 days = 19,345 days\n- Add leap years: 1972, 1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020 (total of 13 leap years) = 19,345 + 13 = 19,358 days.\n- From July 30 to October 5, 2023, is:\n  - August: 31 - 30 = 1 day\n  - September: 30 days\n  - October: 5 days\n  - Total = 1 + 30 + 5 = 36 days.\n\nNow, add 36 days to 19,358 days:\n- Total = 19,358 + 36 = 19,394 days.\n\nTherefore, Christopher Nolan is 19,394 days old as of October 5, 2023.",
#         "generation_info": {
#           "finish_reason": "stop",
#           "model_name": "gpt-4o-mini-2024-07-18",
#           "system_fingerprint": "fp_6fc10e10eb"
#         },
#         "type": "ChatGenerationChunk",
#         "message": {
#           "lc": 1,
#           "type": "constructor",
#           "id": [
#             "langchain",
#             "schema",
#             "messages",
#             "AIMessageChunk"
#           ],
#           "kwargs": {
#             "content": "The 2023 film \"Oppenheimer\" was directed by Christopher Nolan. \n\nTo calculate Christopher Nolan's age in days, we need his birth date. Christopher Nolan was born on July 30, 1970. \n\nLet's calculate his age in days as of today, which is October 5, 2023.\n\n1. Calculate the total number of days from his birth date to today.\n2. From July 30, 1970, to July 30, 2023, is 53 years.\n3. From July 30, 2023, to October 5, 2023, is 2 months and 5 days.\n\nNow, let's break it down:\n\n- 53 years * 365 days = 19,345 days\n- Add leap years: 1972, 1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020 (total of 13 leap years) = 19,345 + 13 = 19,358 days.\n- From July 30 to October 5, 2023, is:\n  - August: 31 - 30 = 1 day\n  - September: 30 days\n  - October: 5 days\n  - Total = 1 + 30 + 5 = 36 days.\n\nNow, add 36 days to 19,358 days:\n- Total = 19,358 + 36 = 19,394 days.\n\nTherefore, Christopher Nolan is 19,394 days old as of October 5, 2023.",
#             "response_metadata": {
#               "finish_reason": "stop",
#               "model_name": "gpt-4o-mini-2024-07-18",
#               "system_fingerprint": "fp_6fc10e10eb"
#             },
#             "type": "AIMessageChunk",
#             "id": "run-126a4673-0003-43fb-a31b-67a63a633e2d",
#             "tool_calls": [],
#             "invalid_tool_calls": []
#           }
#         }
#       }
#     ]
#   ],
#   "llm_output": null,
#   "run": null,
#   "type": "LLMResult"
# }
# [chain/start] [chain:AgentExecutor > chain:RunnableSequence > parser:ToolsAgentOutputParser] Entering Parser run with input:
# [inputs]
# [chain/end] [chain:AgentExecutor > chain:RunnableSequence > parser:ToolsAgentOutputParser] [1ms] Exiting Parser run with output:
# [outputs]
# [chain/end] [chain:AgentExecutor > chain:RunnableSequence] [6.11s] Exiting Chain run with output:
# [outputs]
# [chain/end] [chain:AgentExecutor] [14.12s] Exiting Chain run with output:
# {
#   "output": "The 2023 film \"Oppenheimer\" was directed by Christopher Nolan. \n\nTo calculate Christopher Nolan's age in days, we need his birth date. Christopher Nolan was born on July 30, 1970. \n\nLet's calculate his age in days as of today, which is October 5, 2023.\n\n1. Calculate the total number of days from his birth date to today.\n2. From July 30, 1970, to July 30, 2023, is 53 years.\n3. From July 30, 2023, to October 5, 2023, is 2 months and 5 days.\n\nNow, let's break it down:\n\n- 53 years * 365 days = 19,345 days\n- Add leap years: 1972, 1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020 (total of 13 leap years) = 19,345 + 13 = 19,358 days.\n- From July 30 to October 5, 2023, is:\n  - August: 31 - 30 = 1 day\n  - September: 30 days\n  - October: 5 days\n  - Total = 1 + 30 + 5 = 36 days.\n\nNow, add 36 days to 19,358 days:\n- Total = 19,358 + 36 = 19,394 days.\n\nTherefore, Christopher Nolan is 19,394 days old as of October 5, 2023."
# }
# {
#     'input': 'Who directed the 2023 film Oppenheimer and what is their age in days?',
#     'output': 'The 2023 film "Oppenheimer" was directed by Christopher Nolan. \n\nTo calculate Christopher Nolan\'s age in days, we need his birth date. Christopher Nolan was born on July 30, 
# 1970. \n\nLet\'s calculate his age in days as of today, which is October 5, 2023.\n\n1. Calculate the total number of days from his birth date to today.\n2. From July 30, 1970, to July 30, 
# 2023, is 53 years.\n3. From July 30, 2023, to October 5, 2023, is 2 months and 5 days.\n\nNow, let\'s break it down:\n\n- 53 years * 365 days = 19,345 days\n- Add leap years: 1972, 1976, 1980, 
# 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020 (total of 13 leap years) = 19,345 + 13 = 19,358 days.\n- From July 30 to October 5, 2023, is:\n  - August: 31 - 30 = 1 day\n  - 
# September: 30 days\n  - October: 5 days\n  - Total = 1 + 30 + 5 = 36 days.\n\nNow, add 36 days to 19,358 days:\n- Total = 19,358 + 36 = 19,394 days.\n\nTherefore, Christopher Nolan is 19,394 
# days old as of October 5, 2023.'
# }