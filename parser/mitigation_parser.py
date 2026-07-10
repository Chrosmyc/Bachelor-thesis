from models.mitigation import Mitigation

from parser.markdown_utils import (
    read_md_file,
    split_yaml_and_markdown,
    parse_sections,
    parse_list,
    clean_quote,
    join_list,
)


def parse_mitigation_file(file_path):
    content = read_md_file(file_path)

    metadata, markdown_text = split_yaml_and_markdown(content)
    sections = parse_sections(markdown_text)

    return Mitigation(
        mitigation_id=metadata.get("id", ""),
        paper_id=join_list(metadata.get("papers", [])),
        mitigation_name=metadata.get("title", ""),
        related_risks=metadata.get("related_risks", []),

        mitigation_description=sections.get("Description", ""),
        strategy_type=metadata.get("strategy_type", ""),

        prerequisites=parse_list(sections.get("Prerequisites", "")),
        tools_technologies=parse_list(sections.get("Tools / Technologies", "")),
        tradeoffs_side_effects=parse_list(sections.get("Trade-offs / Side Effects", "")),

        effectiveness=sections.get("Effectiveness", ""),
        probability_of_success=metadata.get("probability_of_success", ""),
        effort_of_mitigation=metadata.get("effort", ""),

        stakeholders=parse_list(sections.get("Stakeholders", "")),
        contextual_constraints=parse_list(sections.get("Contextual Constraints", "")),

        evidence_type=join_list(metadata.get("evidence", [])),
        tags=metadata.get("tags", []),

        standardized_mitigation_entry=sections.get("Standardized Mitigation Entry", ""),
        key_quote=clean_quote(sections.get("Key Quote for Prompting", "")),
        logic_pattern=sections.get("Logic Pattern", ""),
    )