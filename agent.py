import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get Groq API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY is missing. Please add it to your .env file."
    )

# Create Groq client
client = Groq(api_key=api_key)


def generate_code(user_request):
    """
    Generate Python code from a natural-language request.
    """

    prompt = f"""
You are an expert Python developer.

Convert the user's natural-language request into clean,
beginner-friendly Python code.

Requirements:
- Return only the Python code.
- Use clear variable and function names.
- Add helpful comments.
- Make the code executable.
- Do not use Markdown code fences.

User request:
{user_request}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful Python code generation assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=2000
    )

    return response.choices[0].message.content


def main():
    print("=" * 60)
    print("   Natural Language Code Generator")
    print("=" * 60)
    print("Type a request and I will generate Python code.")
    print("Type 'exit' to quit.")
    print()

    while True:
        user_request = input("Enter your request: ").strip()

        if user_request.lower() == "exit":
            print("Goodbye!")
            break

        if not user_request:
            print("Please enter a request.")
            continue

        try:
            print("\nGenerating code...\n")

            code = generate_code(user_request)

            print("-" * 60)
            print(code)
            print("-" * 60)

        except Exception as error:
            print("\nError:", error)


if __name__ == "__main__":
    main()
