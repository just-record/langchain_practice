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

results = structured_llm.invoke("Tell me a joke about cats")
print(results)
# {'setup': 'Why was the cat sitting on the computer?', 'punchline': 'To keep an eye on the mouse!', 'rating': 8}