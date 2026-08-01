"""Extract Risk-, Mitigation- and Relationship-IDs mentioned in a free-text
LLM answer, so an evaluator immediately sees which knowledge base entries
were referenced - without having to read the whole answer manually.

Pure logic only (no Streamlit import here) so it stays easy to unit test.
"""

import re

# "R1", "R23", ... but NOT "Rel1" (no digit right after the "R" in "Rel").
RISK_ID_PATTERN = re.compile(r"\bR(\d+)\b")
# "M1", "M23", ...
MITIGATION_ID_PATTERN = re.compile(r"\bM(\d+)\b")
# "Rel1", "Rel23", ...
RELATIONSHIP_ID_PATTERN = re.compile(r"\bRel(\d+)\b")


def _unique_sorted_ids(pattern: re.Pattern, prefix: str, text: str) -> list[str]:
    numbers = {int(match.group(1)) for match in pattern.finditer(text)}
    return [f"{prefix}{n}" for n in sorted(numbers)]


def extract_mentioned_ids(answer_text: str) -> dict[str, list[str]]:
    """Scan an answer and return every Risk-, Mitigation- and
    Relationship-ID mentioned in it (deduplicated, sorted numerically).

    Example: "See R1, R1 and M12." -> {"risks": ["R1"], "mitigations": ["M12"], "relationships": []}
    """
    if not answer_text:
        return {"risks": [], "mitigations": [], "relationships": []}

    return {
        "risks": _unique_sorted_ids(RISK_ID_PATTERN, "R", answer_text),
        "mitigations": _unique_sorted_ids(MITIGATION_ID_PATTERN, "M", answer_text),
        "relationships": _unique_sorted_ids(RELATIONSHIP_ID_PATTERN, "Rel", answer_text),
    }


def build_known_id_lookup(risks, mitigations, relationships) -> dict[str, dict[str, str]]:
    """Build ID -> short-label lookups from the parsed knowledge base.

    Used to (a) show a readable name next to each extracted ID and
    (b) flag IDs the model mentioned that do not actually exist in the
    dataset (a simple, useful hallucination check for the evaluation).
    """
    risk_labels = {
        risk.risk_id: risk.risk_name
        for risk in risks
        if getattr(risk, "risk_id", "")
    }
    mitigation_labels = {
        mitigation.mitigation_id: mitigation.mitigation_name
        for mitigation in mitigations
        if getattr(mitigation, "mitigation_id", "")
    }
    relationship_labels = {
        relationship.relationship_id: (
            f"{relationship.source_id} → {relationship.target_id} "
            f"({relationship.relationship_type})"
        )
        for relationship in relationships
        if getattr(relationship, "relationship_id", "")
    }
    return {
        "risks": risk_labels,
        "mitigations": mitigation_labels,
        "relationships": relationship_labels,
    }
