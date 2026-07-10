from dataclasses import dataclass


@dataclass
class Relationship:
    relationship_id: str = ""

    source_id: str = ""
    source_type: str = ""   #"risk" or "mitigation"

    target_id: str = ""
    target_type: str = ""   #"risk" or "mitigation"

    relationship_type: str = ""
    influence_strength: str = ""

    secondary_risk_created: str = ""
    applicability_conditions: str = ""
    observed_outcome: str = ""

    evidence_type: str = ""
    confidence_level: str = ""

    reasoning_notes: str = ""
    standardized_relationship_entry: str = ""