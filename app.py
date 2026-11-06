import streamlit as st
from analysis import student_report

from ai_engine import generate_explanation, generate_practice_questions
from history import save_quiz_result, load_history


st.title("AdaptiveAI")
st.write("Your personalized exam preparation assistant")

quiz_results = [
    ("recursion", False),
    ("recursion", True),
    ("recursion", False),
    ("lists", True),
    ("lists", True),
    ("functions", True),
    ("functions", False),
    ("functions", True)
]

report = student_report(quiz_results)

st.subheader("Your Quiz Results")
for topic, score in report["scores"].items():
    st.write(f"{topic.capitalize()}: {score}%")
    st.progress(score / 100)
st.write(report["scores"])


st.subheader("Your Weakest Topic")


st.write(report["weakest_topic"])


st.subheader("Study Recommendations")



st.write(report["recommendations"])





# Challenge 8: Multiple Questions

st.subheader("Python Knowledge Assessment")





questions = [
    {
        "topic": "lists",
        "question": "What does len([10, 20, 30]) return?",
        "options": ["2", "3", "4"],
        "correct": "3",
        "explanation": "len() counts the elements in a list."
    },
    {
        "topic": "lists",
        "question": "What is [5, 10, 15][1]?",
        "options": ["5", "10", "15"],
        "correct": "10",
        "explanation": "Python uses zero-based indexing. Index 1 is 10."
    },
    {
        "topic": "functions",
        "question": "Which keyword defines a Python function?",
        "options": ["func", "def", "function"],
        "correct": "def",
        "explanation": "The def keyword defines a function."
    },
    {
        "topic": "functions",
        "question": "What does a function return without a return statement?",
        "options": ["0", "None", "False"],
        "correct": "None",
        "explanation": "Functions without a return statement return None."
    },
    {
        "topic": "recursion",
        "question": "What is required to stop infinite recursion?",
        "options": ["A loop", "A base case", "A dictionary"],
        "correct": "A base case",
        "explanation": "A base case stops recursive calls."
    },
    {
        "topic": "recursion",
        "question": "What can happen if recursion never reaches its base case?",
        "options": [
            "RecursionError",
            "The function automatically stops",
            "The function returns 0"
        ],
        "correct": "RecursionError",
        "explanation": "Infinite recursion can cause a RecursionError."
    }
]




student_answers = {}

for i, q in enumerate(questions):
    selected_option = st.radio(
        q["question"],
        q["options"],
        index=None,
        key=f"question_{i}"
    )

    student_answers[i] = selected_option







if st.button("Submit Quiz"):

    if any(answer is None for answer in student_answers.values()):
        st.warning("Please answer all questions before submitting.")

    else:
        results = []

        for i, q in enumerate(questions):
            is_correct = (student_answers[i] == q["correct"])

            results.append((q["topic"], is_correct))

        report = student_report(results)

        st.subheader("Quiz Results")
        total_questions = len(results)

        correct_answers = sum(
            is_correct for topic, is_correct in results
        )
        
        accuracy = (correct_answers / total_questions) * 100
        

        save_quiz_result(report, correct_answers, total_questions)

        st.metric(
            "Overall Quiz Score",
            f"{correct_answers}/{total_questions} ({accuracy:.1f}%)"
        )


        
   
  

       

       
        
       

        st.write("Your performance by topic:")

        for topic, score in report["scores"].items():
            st.write(f"{topic.capitalize()}: {score}%")
            st.progress(score / 100)

        weakest = report["weakest_topic"]

        if weakest is None:
            st.success("Excellent! All topics completed successfully.")
        else:
            st.warning(f"You should focus more on {weakest}.")
            
        



        st.subheader("Question Feedback")

        for i, q in enumerate(questions):
            if student_answers[i] == q["correct"]:
                st.success(f"Question {i + 1}: Correct!")
            else:
                st.error(f"Question {i + 1}: Incorrect")

                st.write(f"Your answer: {student_answers[i]}")

                st.write(f"Correct answer: {q['correct']}")

                
                try:
                    with st.spinner("AI is generating your explanation..."):
                        ai_explanation = generate_explanation(
                            q["question"],
                            student_answers[i],
                            q["correct"]
                        )

                    st.info(ai_explanation)

                except Exception:
                    st.warning("AI unavailable. Showing saved explanation.")
                    st.info(q["explanation"])

                
        # Challenge 18: Personalized Study Plan

        study_plans = {
            "lists": [
                "Review list indexing and slicing.",
                "Practice using len(), append(), and remove().",
                "Solve three list manipulation exercises."
            ],
            "functions": [
                "Review parameters and return values.",
                "Practice writing functions with def.",
                "Solve three function exercises."
            ],
            "recursion": [
                "Review how recursive functions work.",
                "Practice identifying base cases.",
                "Solve three recursion exercises."
            ]
        }

        st.subheader("Your Personalized Study Plan")

        weakest = report["weakest_topic"]

        if weakest is None:
            st.success("Great work! Try a harder quiz next.")
        else:
            st.write(f"Focus on: {weakest.capitalize()}")

            for i, task in enumerate(study_plans[weakest], start=1):
                st.write(f"{i}. {task}")
        

st.divider()
st.subheader("AI Practice Questions")

topic = st.selectbox(
    "Choose a topic to practice:",
    ["recursion", "lists", "functions"]
)

if "practice_questions" not in st.session_state:
    st.session_state.practice_questions = []

if st.button("Generate Practice Questions"):
    st.session_state.practice_questions = []

    try:
        with st.spinner("Generating questions with Qwen3..."):
            new_questions = generate_practice_questions(topic)

        st.session_state.practice_questions = new_questions

    
    except Exception as error:
        st.warning(
            "AI generation failed. Showing existing quiz questions instead."
        )

        st.caption(f"Reason: {error}")

        st.session_state.practice_questions = [
            q for q in questions
            if q["topic"] == topic
        ][:2]

   

if st.session_state.practice_questions:
    
    st.info(
        "These are ungraded practice questions. "
        "AI-generated answers may contain mistakes."
    )

    

    for i, q in enumerate(st.session_state.practice_questions):
        st.write(f"Question {i + 1}: {q['question']}")

        for option in q["options"]:
            st.write(f"- {option}")

        with st.expander(f"Show answer {i + 1}"):
            st.write(f"Answer: {q['correct']}")
            st.write(q["explanation"])



# Quiz Progress History

st.divider()
st.subheader("Your Learning Progress")

history = load_history()

if not history:
    st.info("No quiz attempts saved yet.")

else:
    st.write(f"Total attempts: {len(history)}")

    latest = history[-1]
    st.metric(
        "Latest Quiz Score",
        f"{latest['accuracy']}%"
    )

    if len(history) >= 2:
        st.subheader("Performance Over Time")

        accuracies = [
            attempt["accuracy"]
            for attempt in history
        ]

        st.line_chart(accuracies)

    else:
        st.info(
            "Complete another quiz to see your progress chart."
        )







