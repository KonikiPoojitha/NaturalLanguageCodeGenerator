import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("API key missing. Please check your .env file.")
    exit()

client = Groq(api_key=api_key)

print("Natural Language Code Generator")
print("Type 'exit' to quit.")

while True:
    instruction = input("\nEnter your instruction: ")

    if instruction.lower() == "exit":
        print("Goodbye!")
        break

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",                                                      

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a Python code generator. "
                        "Convert the user's natural language instruction "
                        "into correct Python code. "
                        "Return only the Python code, without markdown."
                    )
                },
                {
                    "role": "user",
                    "content": instruction
                }
            ],
            temperature=0
        )

        code = response.choices[0].message.content

        print("\nPython Generated Code:")
        print(code)

    except Exception as e:
        print("\nError:", e)
