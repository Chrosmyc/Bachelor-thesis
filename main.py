from pathlib import Path

from parser.load_all import load_all
from llm.question import ask_question
from llm.show_models import get_models
from evaluation.evaluation import run_evaluation
from graph.knowledge_graph import visualize


# "structured" = normal über die geparsten Markdown-Dateien laden
# "raw" = direkt aus den großen TXT-Dateien in data/raw laden
CONTEXT_SOURCE = "raw"


def load_raw_context():
    raw_folder = Path(__file__).resolve().parent / "data" / "raw"

    risks_file = raw_folder / "Risks.txt"
    mitigations_file = raw_folder / "Mitigations.txt"
    relationship_files = sorted(raw_folder.glob("Relationships_High_*.txt"))

    if not risks_file.exists():
        raise FileNotFoundError(f"Datei nicht gefunden: {risks_file}")

    if not mitigations_file.exists():
        raise FileNotFoundError(f"Datei nicht gefunden: {mitigations_file}")

    if not relationship_files:
        raise FileNotFoundError(
            f"Keine Relationships*.txt-Dateien gefunden in: {raw_folder}"
        )

    risks = risks_file.read_text(
        encoding="utf-8",
        errors="replace"
    )

    mitigations = mitigations_file.read_text(
        encoding="utf-8",
        errors="replace"
    )

    relationships = "\n\n".join(
        (
            f"--- {file_path.name} ---\n"
            f"{file_path.read_text(encoding='utf-8', errors='replace')}"
        )
        for file_path in relationship_files
    )

    return risks, mitigations, relationships


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
    if CONTEXT_SOURCE == "structured":
        risks, mitigations, relationships = load_all()

        print("Loaded Number of Risks:", len(risks))
        print("Loaded Number of Mitigations:", len(mitigations))
        print("Loaded Number of Relationships:", len(relationships))

    elif CONTEXT_SOURCE == "raw":
        risks, mitigations, relationships = load_raw_context()

        print("Loaded raw context from data/raw")
        print("Risk characters:", len(risks))
        print("Mitigation characters:", len(mitigations))
        print("Relationship characters:", len(relationships))

    else:
        raise ValueError(
            'CONTEXT_SOURCE must be either "structured" or "raw".'
        )

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
        relationships
    )
    """


if __name__ == "__main__":
    main()