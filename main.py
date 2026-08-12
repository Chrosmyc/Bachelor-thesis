from pathlib import Path
from parser.load_all import load_all
from llm.question import ask_question
from llm.show_models import get_models
from evaluation.evaluation import run_evaluation
from graph.knowledge_graph import visualize


def load_raw_context():
    raw_folder = Path(__file__).resolve().parent / "data" / "raw"

    risks_file = raw_folder / "Risks.txt"
    mitigations_file = raw_folder / "Mitigations.txt"
    relationship_files = sorted(raw_folder.glob("Relationships_High_*.txt"))

    if not risks_file.exists():
        raise FileNotFoundError(f"File not found: {risks_file}")

    if not mitigations_file.exists():
        raise FileNotFoundError(f"File not found: {mitigations_file}")

    if not relationship_files:
        raise FileNotFoundError(
            f"No Relationships_High_*.txt files found in: {raw_folder}"
        )

    risks = risks_file.read_text(encoding="utf-8", errors="replace")
    mitigations = mitigations_file.read_text(encoding="utf-8", errors="replace")
    relationships = "\n\n".join(
        (
            f"--- {file_path.name} ---\n"
            f"{file_path.read_text(encoding='utf-8', errors='replace')}"
        )
        for file_path in relationship_files
    )

    return risks, mitigations, relationships


def choose_context():
    contexts = [
        ("Full structured context", "full"),
        ("Structured context without relationships", "without_relationships"),
        ("No additional context", "none"),
        ("Unstructured context", "raw"),
    ]

    print("\nAvailable Contexts:")
    for index, (name, _) in enumerate(contexts, start=1):
        print(f"{index}. {name}")

    while True:
        choice = input("\nChoose Context: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(contexts):
            return contexts[int(choice) - 1]

        print("Invalid selection. Please enter a context number.")


def load_context(context_key):
    if context_key == "full":
        return load_all()

    if context_key == "without_relationships":
        risks, mitigations, _ = load_all()
        return risks, mitigations, []

    if context_key == "none":
        return [], [], []

    if context_key == "raw":
        return load_raw_context()

    raise ValueError(f"Unknown context: {context_key}")


def print_context_summary(context_key, risks, mitigations, relationships):
    if context_key == "raw":
        print("Risk characters:", len(risks))
        print("Mitigation characters:", len(mitigations))
        print("Relationship characters:", len(relationships))
        return

    print("Loaded Number of Risks:", len(risks))
    print("Loaded Number of Mitigations:", len(mitigations))
    print("Loaded Number of Relationships:", len(relationships))


def choose_model():
    models = get_models()

    print("\nAvailable Models:")
    for index, model in enumerate(models, start=1):
        print(f"{index}. {model}")

    while True:
        choice = input("\nChoose Model: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(models):
            return models[int(choice) - 1]

        print("Invalid selection. Please enter a model number.")


def main():
    context_name, context_key = choose_context()
    risks, mitigations, relationships = load_context(context_key)

    print(f"\nSelected Context: {context_name}")
    print_context_summary(context_key, risks, mitigations, relationships)

    
    visualize(
        risks,
        mitigations,
        relationships,
    )
    

    model = choose_model()
    print(f"Selected Model: {model}")

    while True:
        question = input("\nEnter Question (or 'exit' to quit): ").strip()

        if question.lower() == "exit":
            print("Program closed.")
            break

        if not question:
            print("Please enter a question.")
            continue

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
        relationships
    )
    """


if __name__ == "__main__":
    main()