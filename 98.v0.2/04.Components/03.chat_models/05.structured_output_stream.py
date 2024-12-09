from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI


llm = ChatOpenAI(model="gpt-3.5-turbo")

json_schema = {
    "title": "joke",
    "description": "Joke to tell user.",
    "type": "object",
    "properties": {
        "setup": {
            "type": "string",
            "description": "The setup of the joke",
        },
        "punchline": {
            "type": "string",
            "description": "The punchline to the joke",
        },
        "rating": {
            "type": "integer",
            "description": "How funny the joke is, from 1 to 10",
        },
    },
    "required": ["setup", "punchline"],
}


structured_llm = llm.with_structured_output(json_schema)

for chunk in structured_llm.stream("Tell me a joke about cats"):
    print(chunk)
# {}
# {'setup': ''}
# {'setup': 'Why'}
# {'setup': 'Why was'}
# {'setup': 'Why was the'}
# {'setup': 'Why was the cat'}
# {'setup': 'Why was the cat sitting'}
# {'setup': 'Why was the cat sitting on'}
# {'setup': 'Why was the cat sitting on the'}
# {'setup': 'Why was the cat sitting on the computer'}
# {'setup': 'Why was the cat sitting on the computer?'}
# {'setup': 'Why was the cat sitting on the computer?', 'punchline': ''}
# {'setup': 'Why was the cat sitting on the computer?', 'punchline': 'It'}
# {'setup': 'Why was the cat sitting on the computer?', 'punchline': 'It wanted'}
# {'setup': 'Why was the cat sitting on the computer?', 'punchline': 'It wanted to'}
# {'setup': 'Why was the cat sitting on the computer?', 'punchline': 'It wanted to keep'}
# {'setup': 'Why was the cat sitting on the computer?', 'punchline': 'It wanted to keep an'}
# {'setup': 'Why was the cat sitting on the computer?', 'punchline': 'It wanted to keep an eye'}
# {'setup': 'Why was the cat sitting on the computer?', 'punchline': 'It wanted to keep an eye on'}
# {'setup': 'Why was the cat sitting on the computer?', 'punchline': 'It wanted to keep an eye on the'}
# {'setup': 'Why was the cat sitting on the computer?', 'punchline': 'It wanted to keep an eye on the mouse'}
# {'setup': 'Why was the cat sitting on the computer?', 'punchline': 'It wanted to keep an eye on the mouse!'}
# {'setup': 'Why was the cat sitting on the computer?', 'punchline': 'It wanted to keep an eye on the mouse!', 'rating': 8}    