
from ollama import chat
import json


def generate_explanation(question, student_answer, correct_answer):

    prompt = f"""
    You are a friendly Python tutor.

    Question: {question}
    Student's answer: {student_answer}
    Correct answer: {correct_answer}

    Explain why the student's answer is incorrect.
    Explain the correct concept in simple English.
    Give one short example.
    Keep your response under 120 words.
    """

    response = chat(
        model="qwen3:1.7b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        think=False
    )

    return response.message.content


def generate_practice_questions(topic):
    
    prompt = f"""
    You are an experienced Python programming teacher.

    Generate exactly 2 multiple-choice questions
    about the Python topic: {topic}

    IMPORTANT RULES:
    1. Ask conceptual questions about Python.
    2. Do NOT ask students to calculate an output.
    3. Do NOT ask questions involving factorial or arithmetic.
    4. Do NOT refer to code that isn't provided.
    5. Each question must have exactly 3 answer options.
    6. Each option must be a possible answer, NOT another question.
    7. Exactly one answer must be correct.
    8. The correct answer must exactly match one option.
    9. Explain why the correct answer is right.
    10. Check that the explanation agrees with the correct answer.
    11.Generate ONLY conceptual questions.
    12. NEVER include Python code snippets in questions or options.
    13. Every answer option must be a short English statement, not a code example.

    Examples of suitable question types:
    - What is the purpose of a base case?
    - What happens when a recursive function calls itself?
    - What is the difference between recursion and iteration?

    Return ONLY valid JSON.

    The JSON object must contain a "questions" list.
    Each question must contain these fields:

    "question": a clear Python question
    "options": a list of exactly 3 possible answers
    "correct": the exact text of the correct option
    "explanation": a short, factually correct explanation

    Generate exactly 2 questions.
    """




    response = chat(
        model="qwen3:1.7b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        format="json",
        think=False
    )
    
    # Show exactly what Qwen3 generated
    print("RAW AI RESPONSE:")
    print(response.message.content)

 

    data = json.loads(response.message.content)
    questions = data["questions"]

    if len(questions) != 2:
        raise ValueError("AI must generate exactly 2 questions.")

    for q in questions:
        if len(q["options"]) != 3:
            raise ValueError("Each question needs 3 options.")
        
        # Reject generated code examples
        for option in q["options"]:
            if "def " in option or "return " in option:
                raise ValueError(
                    "AI generated code instead of conceptual answers."
                )


        if len(set(q["options"])) != 3:
            raise ValueError("Answer options must be different.")

        if q["correct"] not in q["options"]:
            raise ValueError("Correct answer must match an option.")

        if not q["question"] or not q["explanation"]:
            raise ValueError("Question and explanation are required.")

    return questions



# Test our AI engine
if __name__ == "__main__":
    explanation = generate_explanation(
        "What does len([10, 20, 30]) return?",
        "2",
        "3"
    )

    print(explanation)
