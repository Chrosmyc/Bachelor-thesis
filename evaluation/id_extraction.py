"""Extract Risk-, Mitigation- and Relationship-IDs mentioned in a free-text
LLM answer, and provide the FULL documented entry for each one (all fields
from the Risk / Mitigation / Relationship templates), so an evaluator can
directly compare what the model said against the ground truth - a bare
name is not enough to judge correctness.

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


def build_known_id_lookup(risks, mitigations, relationships) -> dict[str, dict[str, object]]:
    """Build ID -> full-object lookups from the parsed knowledge base.

    Storing the whole parsed Risk / Mitigation / Relationship object (not
    just a name) lets the UI show every documented field for an ID, and
    lets us flag IDs the model mentioned that do not exist at all (a
    simple, useful hallucination check for the evaluation).
    """
    risks_by_id = {
        risk.risk_id: risk
        for risk in risks
        if getattr(risk, "risk_id", "")
    }
    mitigations_by_id = {
        mitigation.mitigation_id: mitigation
        for mitigation in mitigations
        if getattr(mitigation, "mitigation_id", "")
    }
    relationships_by_id = {
        relationship.relationship_id: relationship
        for relationship in relationships
        if getattr(relationship, "relationship_id", "")
    }
    return {
        "risks": risks_by_id,
        "mitigations": mitigations_by_id,
        "relationships": relationships_by_id,
    }


def _val(value) -> str:
    """Render a single field: '–' if it is empty/None, otherwise as-is."""
    if value is None or value == "":
        return "–"
    return str(value)


def _list_val(values) -> str:
    """Render a list field as a comma-separated string, '–' if empty."""
    if not values:
        return "–"
    return ", ".join(str(v) for v in values)


def label_for(section_key: str, obj) -> str:
    """Short human-readable label used as the expander title for an ID."""
    if obj is None:
        return "not found in knowledge base"
    if section_key == "risks":
        return obj.risk_name or "–"
    if section_key == "mitigations":
        return obj.mitigation_name or "–"
    if section_key == "relationships":
        return f"{obj.source_id} → {obj.target_id} ({_val(obj.relationship_type)})"
    return "–"


def format_risk_details(risk) -> str:
    """Render every field of the RISK IDENTIFICATION template as Markdown."""
    return (
        f"- **Risk Name:** {_val(risk.risk_name)}\n"
        f"- **Dimension:** {_val(risk.dimension)}  |  **Granularity Level:** {_val(risk.granularity_level)}\n"
        f"- **Modernization Strategy:** {_val(risk.modernization_strategy)}\n"
        f"- **Risk Description:** {_val(risk.risk_description)}\n"
        f"- **Root Cause / Challenge:** {_val(risk.root_cause)}\n"
        f"- **Trigger Event:** {_val(risk.trigger_event)}\n"
        f"- **Impact / Consequences:** {_val(risk.impact)}\n"
        f"- **Linked Risks:** {_list_val(risk.linked_risks)}\n"
        f"- **Stakeholders:** {_list_val(risk.stakeholders)}\n"
        f"- **Contextual Constraints:** {_list_val(risk.contextual_constraints)}\n"
        f"- **Evidence Type:** {_val(risk.evidence_type)}  |  **Detection Source:** {_val(risk.detection_source)}\n"
        f"- **Key Terminology (Tags):** {_list_val(risk.tags)}\n"
        f"- **Standardized Risk Entry:** {_val(risk.standardized_risk_entry)}\n"
        f"- **Key Quote for Prompting:** {_val(risk.key_quote)}\n"
        f"- **Logic Pattern:** {_val(risk.logic_pattern)}\n"
        f"- **Paper ID:** {_val(risk.paper_id)}"
    )


def format_mitigation_details(mitigation) -> str:
    """Render every field of the MITIGATION STRATEGY template as Markdown."""
    return (
        f"- **Mitigation Name:** {_val(mitigation.mitigation_name)}\n"
        f"- **Related Risks:** {_list_val(mitigation.related_risks)}\n"
        f"- **Mitigation Description:** {_val(mitigation.mitigation_description)}\n"
        f"- **Strategy Type:** {_val(mitigation.strategy_type)}\n"
        f"- **Prerequisites:** {_list_val(mitigation.prerequisites)}\n"
        f"- **Tools / Technologies:** {_list_val(mitigation.tools_technologies)}\n"
        f"- **Trade-offs / Side Effects:** {_list_val(mitigation.tradeoffs_side_effects)}\n"
        f"- **Effectiveness:** {_val(mitigation.effectiveness)}\n"
        f"- **Probability of Success:** {_val(mitigation.probability_of_success)}  |  "
        f"**Effort of Mitigation:** {_val(mitigation.effort_of_mitigation)}\n"
        f"- **Stakeholders:** {_list_val(mitigation.stakeholders)}\n"
        f"- **Contextual Constraints:** {_list_val(mitigation.contextual_constraints)}\n"
        f"- **Evidence Type:** {_val(mitigation.evidence_type)}\n"
        f"- **Key Terminology (Tags):** {_list_val(mitigation.tags)}\n"
        f"- **Standardized Mitigation Entry:** {_val(mitigation.standardized_mitigation_entry)}\n"
        f"- **Key Quote for Prompting:** {_val(mitigation.key_quote)}\n"
        f"- **Logic Pattern:** {_val(mitigation.logic_pattern)}\n"
        f"- **Paper ID:** {_val(mitigation.paper_id)}"
    )


def format_relationship_details(relationship) -> str:
    """Render every field of the RISK-MITIGATION RELATIONSHIP template as Markdown."""
    return (
        f"- **Source:** {_val(relationship.source_id)} ({_val(relationship.source_type)})\n"
        f"- **Target:** {_val(relationship.target_id)} ({_val(relationship.target_type)})\n"
        f"- **Relationship Type:** {_val(relationship.relationship_type)}\n"
        f"- **Influence Strength:** {_val(relationship.influence_strength)}\n"
        f"- **Secondary Risk Created:** {_val(relationship.secondary_risk_created)}\n"
        f"- **Applicability Conditions:** {_val(relationship.applicability_conditions)}\n"
        f"- **Observed Outcome:** {_val(relationship.observed_outcome)}\n"
        f"- **Evidence Type:** {_val(relationship.evidence_type)}  |  "
        f"**Confidence Level:** {_val(relationship.confidence_level)}\n"
        f"- **Reasoning Notes:** {_val(relationship.reasoning_notes)}\n"
        f"- **Standardized Relationship Entry:** {_val(relationship.standardized_relationship_entry)}"
    )


DETAIL_FORMATTERS = {
    "risks": format_risk_details,
    "mitigations": format_mitigation_details,
    "relationships": format_relationship_details,
}


def format_details(section_key: str, obj) -> str:
    """Dispatch to the right formatter for a given section ('risks',
    'mitigations' or 'relationships')."""
    formatter = DETAIL_FORMATTERS[section_key]
    return formatter(obj)