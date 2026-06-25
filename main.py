import os
import json
from dotenv import load_dotenv
from groq import Groq

from memory import memory_manager
from guardrails import validate_question

load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found in .env file"
    )

client = Groq(
    api_key=GROQ_API_KEY
)

MODEL = "llama-3.3-70b-versatile"


SYSTEM_PROMPT = """
You are Student Study Helper.

You are an expert tutor in:

- Mathematics
- Statistics
- Probability
- Algebra
- Calculus
- Linear Algebra

Your responsibility is to teach students
step-by-step.

Always explain your reasoning clearly.

Always return VALID JSON ONLY.

Return JSON using EXACTLY this format:

{
    "topic": "",
    "steps": [
        ""
    ],
    "final_answer": "",
    "confidence": ""
}

Rules:

1. Explain solutions step-by-step.
2. Use simple language.
3. Show calculations when possible.
4. Do not return markdown.
5. Do not return code blocks.
6. Return JSON only.
"""



def build_context(session_id: str):

    context = memory_manager.get_context(
        session_id
    )

    if not context:
        return "No previous conversation."

    return context


def ask_groq(question, context):

    user_prompt = f"""
Previous Conversation:

{context}

Current Question:

{question}

Provide a step-by-step educational solution.
"""

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    return (
        response
        .choices[0]
        .message
        .content
        .strip()
    )


def parse_response(response_text):

    try:

        return json.loads(response_text)

    except Exception:

        return {
            "topic": "Solution",
            "steps": [
                "Unable to parse model response."
            ],
            "final_answer": response_text,
            "confidence": "Low"
        }



def solve_question(
    question: str,
    session_id: str = "default"
):


    valid, message = validate_question(
        question
    )

    if not valid:

        return {
            "topic": "Rejected",
            "steps": [],
            "final_answer": message,
            "confidence": "Low"
        }



    context = build_context(
        session_id
    )


    raw_response = ask_groq(
        question,
        context
    )

    

    result = parse_response(
        raw_response
    )

    

    memory_manager.save(
        session_id=session_id,
        question=question,
        answer=result
    )

    return result



if __name__ == "__main__":

    print(
        "\nStudent Study Helper Started\n"
    )

    while True:

        question = input(
            "\nAsk a question: "
        )

        if question.lower() == "exit":
            break

        result = solve_question(
            question=question,
            session_id="test_user"
        )

        print(
            json.dumps(
                result,
                indent=4
            )
        )