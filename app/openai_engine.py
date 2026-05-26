from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def ask_hydrokrat(user_prompt):

    system_prompt = """
You are Hydrokrat AI.

You are a professional KSB pump selection engineer.

Your job:
- Recommend KSB pumps
- Explain hydraulic concepts
- Help with HVAC
- Help with Fire Fighting systems
- Help with Borewell pumps
- Help with sewage pumps
- Help with pressure boosting
- Recommend pumps using engineering logic

Always respond professionally.
Always prefer KSB pump families.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content