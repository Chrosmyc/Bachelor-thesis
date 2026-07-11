from parser.load_all import load_all
from llm.question import ask_question


def main():
    risks, mitigations, relationships = load_all()

    print("Loaded Number of Risks:", len(risks))
    print("Loaded Number of Mitigations:", len(mitigations))
    print("Loaded Number of Relationships:", len(relationships))

    question = input("\nEnter Question: ")

    answer = ask_question(
        question,
        risks,
        mitigations,
        relationships
    )

    print("\nAnswer:")
    print(answer)


if __name__ == "__main__":
    main()