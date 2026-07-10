from pathlib import Path

from parser.risk_parser import parse_risk_file
from parser.mitigation_parser import parse_mitigation_file
from parser.relationship_parser import parse_relationship_file


def load_all_risks(folder_path="data/risks"):
    risks = []

    for file_path in Path(folder_path).glob("*.md"):
        risk = parse_risk_file(file_path)
        risks.append(risk)

    return risks


def load_all_mitigations(folder_path="data/mitigations"):
    mitigations = []

    for file_path in Path(folder_path).glob("*.md"):
        mitigation = parse_mitigation_file(file_path)
        mitigations.append(mitigation)

    return mitigations


def load_all_relationships(folder_path="data/relationships"):
    relationships = []

    for file_path in Path(folder_path).glob("*.md"):
        relationship = parse_relationship_file(file_path)
        relationships.append(relationship)

    return relationships


def load_all():
    risks = load_all_risks()
    mitigations = load_all_mitigations()
    relationships = load_all_relationships()
    return risks, mitigations, relationships