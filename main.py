from parser.load_all import load_all
from llm.question import ask_question
from llm.show_models import get_models
from evaluation.evaluation import run_evaluation
from graph.knowledge_graph import visualize

def choose_model():
    models = get_models()

    print("\nAvailable Models:")
    for index, model in enumerate(models, start=1):
        print(f"{index}. {model}")

    while True:
        choice = input("\nChoose Model: ")

        if choice.isdigit() and 1 <= int(choice) <= len(models):
            return models[int(choice) - 1]

        print("Invalid selection. Please enter a model number.")

def main():
    risks, mitigations, relationships = load_all()

    print("Loaded Number of Risks:", len(risks))
    print("Loaded Number of Mitigations:", len(mitigations))
    print("Loaded Number of Relationships:", len(relationships))
    """
    visualize(
        risks,
        mitigations,
        relationships,
    )
    """

    model = choose_model()
    while True:
        question = input("\nEnter Question: ")

        answer = ask_question(
            question,
            risks,
            mitigations,
            relationships,
            model
        )

        print("\nAnswer:")
        print(answer)

    """
    run_evaluation(
        risks,
        mitigations,
        relationship
    )   
    """

if __name__ == "__main__":
    main()