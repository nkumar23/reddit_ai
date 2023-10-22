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
chunk_size = 5  # Number of posts per chunk
chunks = [data[i : i + chunk_size] for i in range(0, len(data), chunk_size)]

messages = [{"role": "system", "content": "You are a helpful assistant."}]

# Send each chunk as context
for chunk in chunks:
    chunk_string = json.dumps(chunk)
    messages.append({"role": "user", "content": chunk_string})

# Now, after all chunks have been sent as context, ask for the recommendation
messages.append(
    {
        "role": "user",
        "content": "Based on the provided data from Reddit about basketball, provide a recommendation for new topics for educational programming at the NBA Hall of Fame museum.",
    }
)

completion = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k", messages=messages)

response = completion.choices[0].message["content"]
print(response)
