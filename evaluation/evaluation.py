from .evaluation_questions import QUESTIONS
from llm.question import ask_question
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")


def run_evaluation(risks, mitigations, relationships):
    print(f"Starting evaluation with {len(QUESTIONS)} questions.")

    for index, question in enumerate(QUESTIONS, start=1):
        print("\n" + "=" * 80)
        print(f"QUESTION {index}/{len(QUESTIONS)}")
        print("=" * 80)
        print(question)

        try:
            answer = ask_question(
                question,
                risks,
                mitigations,
                relationships
            )

            print("\nANSWER:")
            print(answer)

        except Exception as error:
            print("\nERROR:")
            print(error)

    print("\n" + "=" * 80)
    print("EVALUATION COMPLETED")
    print("=" * 80)