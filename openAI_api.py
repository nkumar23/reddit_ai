import openai
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access secrets from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Call OpenAI API to summarize info
openai.api_key = OPENAI_API_KEY

# load in JSON data generated in "reddit_data_extract.py" code

with open("reddit_data.json", "r", encoding="utf-8") as jsonfile:
    json_string = jsonfile.read()

data = json.loads(json_string)

# call OpenAI API with prompt and JSON data

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "The following data is a JSON file containing posts and comments information from the NYC Transit subreddit on Reddit. Then provide a recommendation for new topics for educational programming at a transit museum based on the Reddit comments.",
        },
        {"role": "user", "content": str(data)},
    ],
)

# print output to console

completion_data = completion.choices[0].message
content = completion_data["content"]

lines = content.split("\n")
for line in lines:
    print(f"--> {line}")
