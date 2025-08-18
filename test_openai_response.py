from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-4o",
    tools=[{"type": "web_search_preview"}],
    input="canadagoose jacket blue"
)

print(response.output_text)

import IPython
IPython.embed()