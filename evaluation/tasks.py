"""Fixed evaluation tasks shown to experts in the Streamlit app.

Having them here as a plain dict lets the app offer a dropdown so experts
can pick a task instead of copy-pasting it from a separate cheat sheet.
Edit the text below if a task wording changes - the app picks it up
automatically, nothing else needs to change.
"""

TASKS = {
    "Task 1 – Risk Information Retrieval": (
        "What are the root cause, trigger event, impact, and stakeholders of "
        "R1 - Incomplete or Erroneous Data Migration?"
    ),
    "Task 2 – Direct Risk–Mitigation Relationships": (
        "Explain the documented relationships between:\n"
        "- R1 - Incomplete or Erroneous Data Migration and M1 - Data Migration Strategy\n"
        "- R2 - Scarcity of Experts and Documentation and M2 - Automated Logic Extraction"
    ),
    "Task 3 – Indirect Risk Chain": (
        "Create and explain a risk chain from R2 - Scarcity of Experts and "
        "Documentation through R3 - Time Overrun to R4 - Cost Overrun."
    ),
    "Task 4 – Scenario-Based Analysis": (
        "A company migrates data from an obsolete non-relational database with "
        "incomplete documentation. In addition, several legacy experts will "
        "retire before the modernization project is completed.\n"
        "Identify the relevant risks, mitigation strategies, and relationships."
    ),
    "Task 5 – Evaluation of Unsupported or Incorrect Statements": (
        "Evaluate the following statements based on the documented information. "
        "Correct each statement where necessary and clearly state when "
        "information is not documented.\n"
        "a. What is the exact percentage probability that M1 - Data Migration "
        "Strategy will prevent R1 - Incomplete or Erroneous Data Migration?\n"
        "b. M6 - Proof of Concept guarantees that modernization project failure "
        "will be completely eliminated.\n"
        "c. M14 - Component Decoupling prevents R18 - Orchestration and "
        "Complexity Explosion."
    ),
    "Task 6 – Machine-Readable Output": (
        "Create a machine-readable risk chain for R2 → R3 → R4 as valid JSON.\n"
        "Include all available:\n"
        "- Risk IDs\n"
        "- Mitigation IDs\n"
        "- Relationship IDs\n"
        "- Relationship types\n"
        "- Confidence levels\n"
        "Clearly represent information that is not documented without inventing values."
    ),
}
