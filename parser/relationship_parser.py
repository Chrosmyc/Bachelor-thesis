from models.relationship import Relationship

from parser.markdown_utils import (
    read_md_file,
    split_yaml_and_markdown,
    parse_sections,
)


def parse_relationship_file(file_path):
    content = read_md_file(file_path)

    metadata, markdown_text = split_yaml_and_markdown(content)
    sections = parse_sections(markdown_text)

    source_id = ""
    source_type = ""
    target_id = ""
    target_type = ""

    if metadata.get("source_risk_id"):
        source_id = metadata.get("source_risk_id", "")
        source_type = "risk"

    if metadata.get("source_mitigation_id"):
        source_id = metadata.get("source_mitigation_id", "")
        source_type = "mitigation"

    if metadata.get("target_risk_id"):
        target_id = metadata.get("target_risk_id", "")
        target_type = "risk"

    if metadata.get("target_mitigation_id"):
        target_id = metadata.get("target_mitigation_id", "")
        target_type = "mitigation"

    return Relationship(
        relationship_id=metadata.get("id", ""),

        source_id=source_id,
        source_type=source_type,

        target_id=target_id,
        target_type=target_type,

        relationship_type=metadata.get("relationship_type", ""),
        influence_strength=metadata.get("influence_strength", ""),

        secondary_risk_created=sections.get("Secondary Risk Created","",),
        applicability_conditions=sections.get("Applicability Conditions", ""),
        observed_outcome=sections.get("Observed Outcome", ""),

        evidence_type=metadata.get("evidence_type", ""),
        confidence_level=metadata.get("confidence_level", ""),

        reasoning_notes=sections.get("Reasoning Notes", ""),
        standardized_relationship_entry=sections.get("Standardized Relationship Entry", ""),
    )