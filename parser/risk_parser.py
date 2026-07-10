from models.risk import Risk

from parser.markdown_utils import (
    read_md_file,
    split_yaml_and_markdown,
    parse_sections,
    parse_list,
    clean_quote,
    join_list,
)


def parse_risk_file(file_path):
    content = read_md_file(file_path)

    metadata, markdown_text = split_yaml_and_markdown(content)
    sections = parse_sections(markdown_text)

    return Risk(
        risk_id=metadata.get("id", ""),
        paper_id=join_list(metadata.get("papers", [])),
        risk_name=metadata.get("title", ""),
        risk_description=sections.get("Description", ""),
        modernization_strategy=join_list(metadata.get("strategy", [])),
        dimension=metadata.get("dimension", ""),
        granularity_level=metadata.get("granularity", ""),

        root_cause=sections.get("Root Cause", ""),
        trigger_event=sections.get("Trigger Event", ""),
        impact=sections.get("Impact", ""),

        linked_risks=parse_list(sections.get("Linked Risks", "")),
        stakeholders=parse_list(sections.get("Stakeholders", "")),
        contextual_constraints=parse_list(sections.get("Contextual Constraints", "")),

        evidence_type=join_list(metadata.get("evidence", [])),
        detection_source=sections.get("Detection Source", ""),
        tags=metadata.get("tags", []),

        standardized_risk_entry=sections.get("Standardized Risk Entry", ""),
        key_quote=clean_quote(sections.get("Key Quote for Prompting", "")),
        logic_pattern=sections.get("Logic Pattern", ""),
    )