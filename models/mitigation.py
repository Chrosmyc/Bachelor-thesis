from dataclasses import dataclass, field


@dataclass
class Mitigation:
    mitigation_id: str = ""
    paper_id: str = ""
    mitigation_name: str = ""
    related_risks: list[str] = field(default_factory=list)

    mitigation_description: str = ""
    strategy_type: str = ""

    prerequisites: list[str] = field(default_factory=list)
    tools_technologies: list[str] = field(default_factory=list)
    tradeoffs_side_effects: list[str] = field(default_factory=list)

    effectiveness: str = ""
    probability_of_success: str = ""
    effort_of_mitigation: str = ""

    stakeholders: list[str] = field(default_factory=list)
    contextual_constraints: list[str] = field(default_factory=list)

    evidence_type: str = ""
    tags: list[str] = field(default_factory=list)

    standardized_mitigation_entry: str = ""
    key_quote: str = ""
    logic_pattern: str = ""