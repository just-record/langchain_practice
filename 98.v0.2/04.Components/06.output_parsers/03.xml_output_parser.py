### 모델에 따라서 json보다 xml 출력이 나은 경우도 있다.
### Anthropic의 모델은 XML을 권장한다.
from dotenv import load_dotenv
load_dotenv()

from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import XMLOutputParser
from langchain_core.prompts import PromptTemplate

model = ChatAnthropic(model="claude-2.1", max_tokens_to_sample=512, temperature=0.1)

actor_query = "Generate the shortened filmography for Tom Hanks."


### 1. parset 없이 간단한 요청
output = model.invoke(
    f"""{actor_query}
Please enclose the movies in <movie></movie> tags"""
)

print(output.content)
# Here is the shortened filmography for Tom Hanks, enclosed in XML tags:

# <movie>Splash</movie>
# <movie>Big</movie>
# <movie>A League of Their Own</movie>
# <movie>Sleepless in Seattle</movie>
# <movie>Forrest Gump</movie>
# <movie>Toy Story</movie>
# <movie>Apollo 13</movie>
# <movie>Saving Private Ryan</movie>
# <movie>Cast Away</movie>
# <movie>The Da Vinci Code</movie>
# <movie>Captain Phillips</movie>


### 2. parser = XMLOutputParser()
print('-'*30)
parser = XMLOutputParser()

# We will add these instructions to the prompt below
print(f'parser.get_format_instructions(): {parser.get_format_instructions()}')
print('-'*30)
# parser.get_format_instructions(): The output should be formatted as a XML file.
# 1. Output should conform to the tags below. 
# 2. If tags are not given, make them on your own.
# 3. Remember to always open and close all the tags.

# As an example, for the tags ["foo", "bar", "baz"]:
# 1. String "<foo>
#    <bar>
#       <baz></baz>
#    </bar>
# </foo>" is a well-formatted instance of the schema. 
# 2. String "<foo>
#    <bar>
#    </foo>" is a badly-formatted instance.
# 3. String "<foo>
#    <tag>
#    </tag>
# </foo>" is a badly-formatted instance.

# Here are the output tags:
# ```
# None
# ```

prompt = PromptTemplate(
    template="""{query}\n{format_instructions}""",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | model | parser

output = chain.invoke({"query": actor_query})
print(output)
# {'filmography': [{'movie': [{'title': 'Big'}, {'year': '1988'}]}, {'movie': [{'title': 'Forrest Gump'}, {'year': '1994'}]}, {'movie': [{'title': 'Toy Story'}, {'year': '1995'}]}, {'movie': [{'title': 'Saving Private Ryan'}, {'year': '1998'}]}, {'movie': [{'title': 'Cast Away'}, {'year': '2000'}]}]}


### 3. 사용자 필요에 맞는 tags 추가하기
print('-'*30)
parser = XMLOutputParser(tags=["movies", "actor", "film", "name", "genre"])
# parser.get_format_instructions(): The output should be formatted as a XML file.
# 1. Output should conform to the tags below. 
# 2. If tags are not given, make them on your own.
# 3. Remember to always open and close all the tags.

# As an example, for the tags ["foo", "bar", "baz"]:
# 1. String "<foo>
#    <bar>
#       <baz></baz>
#    </bar>
# </foo>" is a well-formatted instance of the schema. 
# 2. String "<foo>
#    <bar>
#    </foo>" is a badly-formatted instance.
# 3. String "<foo>
#    <tag>
#    </tag>
# </foo>" is a badly-formatted instance.

# Here are the output tags:
# ```
# ['movies', 'actor', 'film', 'name', 'genre']
# ```

# We will add these instructions to the prompt below
print(f'parser.get_format_instructions(): {parser.get_format_instructions()}')
print('-'*30)
# {'movies': [{'actor': [{'name': 'Tom Hanks'}, {'film': [{'name': 'Forrest Gump'}, {'genre': 'Drama'}]}, {'film': [{'name': 'Cast Away'}, {'genre': 'Adventure'}]}, {'film': [{'name': 'Saving Private Ryan'}, {'genre': 'War'}]}]}]}

prompt = PromptTemplate(
    template="""{query}\n{format_instructions}""",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)


chain = prompt | model | parser

output = chain.invoke({"query": actor_query})

print(output)


### 4. streaming 사용하기
print('-'*30)
for s in chain.stream({"query": actor_query}):
    print(s)
# {'movies': [{'actor': [{'name': 'Tom Hanks'}]}]}
# {'movies': [{'actor': [{'film': [{'name': 'Forrest Gump'}]}]}]}
# {'movies': [{'actor': [{'film': [{'genre': 'Drama'}]}]}]}
# {'movies': [{'actor': [{'film': [{'name': 'Cast Away'}]}]}]}
# {'movies': [{'actor': [{'film': [{'genre': 'Adventure'}]}]}]}
# {'movies': [{'actor': [{'film': [{'name': 'The Green Mile'}]}]}]}
# {'movies': [{'actor': [{'film': [{'genre': 'Drama'}]}]}]}    