
import json
from pathlib import Path
from datetime import datetime

HISTORY_FILE = Path(__file__).with_name("quiz_history.json")


def load_history():
    if not HISTORY_FILE.exists():
        return []

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_quiz_result(report, correct_answers, total_questions):
    history = load_history()

    new_result = {
        "date": datetime.now().astimezone().isoformat(
            timespec="seconds"
        ),
        "correct_answers": correct_answers,
        "total_questions": total_questions,
        "accuracy": round(correct_answers / total_questions * 100, 1),
        "scores": report["scores"],
        "weakest_topic": report["weakest_topic"]
    }

    history.append(new_result)

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)

    return new_result
