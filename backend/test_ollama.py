from ollama import Client

client = Client(host="http://localhost:11434")

response = client.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "user",
            "content": "Say Hello"
        }
    ]
)

print(response)