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
### 1. set_verbose
### 입력과 출력이 좀 더 읽기 쉬운 형식으로 출력되며, 특정 원시 출력(LLM 호출의 토큰 사용 통계와 같은)의 로깅을 건너뛰어 애플리케이션 로직에 집중
print('1.', '-' * 50)
##################################################################################
from langchain.globals import set_verbose

set_verbose(True)
agent_executor = AgentExecutor(agent=agent, tools=tools)
results = agent_executor.invoke(
    {"input": "Who directed the 2023 film Oppenheimer and what is their age in days?"}
)
rprint(results)
# 1. --------------------------------------------------


# > Entering new AgentExecutor chain...

# Invoking: `tavily_search_results_json` with `{'query': 'Oppenheimer 2023 film director'}`


# [{'url': 'https://www.imdb.com/title/tt15398776/fullcredits/', 'content': 'Oppenheimer (2023) cast and crew credits, including actors, actresses, directors, writers and more. Menu. ... director of photography: behind-the-scenes Jason Gary ... best boy grip ... film loader Luc Poullain ... aerial coordinator'}]
# Invoking: `tavily_search_results_json` with `{'query': 'Oppenheimer 2023 film release date'}`


# [{'url': 'https://www.rottentomatoes.com/m/oppenheimer_2023', 'content': "Genre:\nHistory,\nDrama,\nBiography\nOriginal Language:\nEnglish\nDirector:\nChristopher Nolan\nProducer:\nEmma Thomas,\nCharles Roven,\nChristopher Nolan\nWriter:\nChristopher Nolan\nRelease Date (Theaters):\nJul 21, 2023\nwide\nRelease Date (Streaming):\nNov 21, 2023\nBox Office (Gross USA):\n$328.1M\nRuntime:\n3h 0m\nDistributor:\nUniversal Pictures\nProduction Co:\nGadget Films,\nUniversal Pictures,\nSyncopy,\nAtlas Entertainment\nSound Mix:\nDatasat, Dolby Digital\nCast & Crew\nCillian Murphy\nJ. Robert Oppenheimer\nEmily Blunt\nKitty Oppenheimer\nRobert Downey Jr.\nLewis Strauss\nMatt Damon\nLeslie Groves Jr.\nRami Malek\nDavid Hill\nFlorence Pugh\nJean Tatlock\nBenny Safdie\nEdward Teller\nMichael Angarano\nRobert Serber\nJosh Hartnett\nErnest Lawrence\nKenneth Branagh\nNiels Bohr\nCasey Affleck\nBoris Pash\n Dane DeHaan\nKenneth Nichols\nDylan Arnold\nFrank Oppenheimer\nDavid Krumholtz\nIsidor Rabi\nAlden Ehrenreich\nSenate Aide\nMatthew Modine\nVannevar Bush\nJosh Peck\nKenneth Bainbridge\nGary Oldman\nHarry Truman\nJason Clarke\nJack Quaid\nChristopher Nolan\nDirector\nChristopher Nolan\nScreenwriter\nEmma Thomas\nProducer\nCharles Roven\nProducer\nChristopher Nolan\nProducer\nHoyte Van Hoytema\nCinematographer\nJennifer Lame\nFilm Editing\nLudwig Göransson\nOriginal Music\nNews & Interviews for Oppenheimer\nAwards Leaderboard: Top Movies of 2023\nOscar Nominations 2024: The Complete List of Nominees\nRotten Tomatoes Predicts the 2024 Oscar Nominations\nCritic Reviews for Oppenheimer\nAudience Reviews for Oppenheimer\nThere are no featured audience reviews for Oppenheimer at this time.\n Movies / TV\nCelebrity\nNo Results Found\nMovies in theaters\nMovies at home\nMore\nCertified fresh picks\nNew TV Tonight\nMost Popular TV on RT\nMore\nCertified fresh pick\nColumns\nGuides\n65 Movies That Celebrate Black Joy\n100 Best Free Movies on YouTube (February 2024)\n Hubs\nBlack Heritage\nGolden Tomato Awards: Best Movies & TV of 2023\nRT News\n10 Films About Black Music That Turn Household Names into Household Stories\nMr. & Mrs. Smith First Reviews: Donald Glover & Maya Erskine Shine in ‘Compelling’ Reboot, Critics Say\nOppenheimer\n2023, History/Drama, 3h 0m\nWhat to know\nCritics Consensus\nOppenheimer marks another engrossing achievement from Christopher Nolan that benefits from Murphy's tour-de-force performance and stunning visuals.\n Movie & TV guides\nPlay Daily Tomato Movie Trivia\nAwards Tour\nDiscover What to Watch\nRotten Tomatoes Podcasts\nJoin The Newsletter\nGet the freshest reviews, news, and more delivered right to your inbox!\n"}]The 2023 film "Oppenheimer" was directed by Christopher Nolan. 

# Christopher Nolan was born on July 30, 1970. To calculate his age in days as of today, October 5, 2023:

# 1. From July 30, 1970, to July 30, 2023, is 53 years.
# 2. From July 30, 2023, to October 5, 2023, is an additional 66 days.

# Now, let's calculate the total days:

# - 53 years = 53 * 365 = 19,445 days (not accounting for leap years yet).
# - We also need to consider leap years. From 1970 to 2023, there are 13 leap years (1972, 1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020).
# - So, we add 13 days for leap years: 19,445 + 13 = 19,458 days.
# - Finally, we add the additional 66 days: 19,458 + 66 = 19,524 days.

# Thus, Christopher Nolan is 19,524 days old as of October 5, 2023.

# > Finished chain.
# {
#     'input': 'Who directed the 2023 film Oppenheimer and what is their age in days?',
#     'output': 'The 2023 film "Oppenheimer" was directed by Christopher Nolan. \n\nChristopher Nolan was born on July 30, 1970. To calculate his age in days as of today, October 5, 2023:\n\n1. 
# From July 30, 1970, to July 30, 2023, is 53 years.\n2. From July 30, 2023, to October 5, 2023, is an additional 66 days.\n\nNow, let\'s calculate the total days:\n\n- 53 years = 53 * 365 = 
# 19,445 days (not accounting for leap years yet).\n- We also need to consider leap years. From 1970 to 2023, there are 13 leap years (1972, 1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 
# 2012, 2016, 2020).\n- So, we add 13 days for leap years: 19,445 + 13 = 19,458 days.\n- Finally, we add the additional 66 days: 19,458 + 66 = 19,524 days.\n\nThus, Christopher Nolan is 19,524 
# days old as of October 5, 2023.'
# }