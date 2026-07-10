from dataclasses import dataclass, field


@dataclass
class Risk:
    risk_id: str = ""
    paper_id: str = ""
    risk_name: str = ""
    risk_description: str = ""
    modernization_strategy: str = ""
    dimension: str = ""
    granularity_level: str = ""

    root_cause: str = ""
    trigger_event: str = ""
    impact: str = ""

    linked_risks: list[str] = field(default_factory=list)
    stakeholders: list[str] = field(default_factory=list)
    contextual_constraints: list[str] = field(default_factory=list)

    evidence_type: str = ""
    detection_source: str = ""
    tags: list[str] = field(default_factory=list)

    standardized_risk_entry: str = ""
    key_quote: str = ""
    logic_pattern: str = ""