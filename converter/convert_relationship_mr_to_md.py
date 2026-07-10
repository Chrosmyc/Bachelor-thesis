from pathlib import Path
import re


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent

INPUT_FILE = PROJECT_DIR /  "data" / "raw" / "Relationships_Mitigation_Risk.txt"
OUTPUT_FOLDER = PROJECT_DIR / "data" / "relationships"
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


with open(INPUT_FILE, "r", encoding="utf-8") as f:
    content = f.read()

risk_blocks = re.split(r'(?=Relationship ID:)', content)
risk_blocks = [block.strip() for block in risk_blocks if block.strip()]

def create_markdown(data):
    import re

    markdown = f"""---
id: {data.get("Relationship ID","")}
type: Relationship

source_mitigation_id: {data.get("Source Mitigation ID","")}
source_risk_id: {data.get("Target Risk ID","")}

relationship_type: {data.get("Relationship Type","")}
influence_strength: {data.get("Influence Strength","")}
confidence_level: {data.get("Confidence Level","")}

evidence_type: {data.get("Evidence Type","")}


# Applicability Conditions
{data.get("Applicability Conditions","")}

# Observed Outcome
{data.get("Observed Outcome","")}

# Reasoning Notes
{data.get("Reasoning Notes","")}

# Standardized Relationship Entry
{data.get("Standardized Relationship Entry","")}
"""
    return markdown


for block in risk_blocks:
    data = {}
    
    for line in block.splitlines():
        line = line.strip()

        if not line:
            continue

        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()

    markdown = create_markdown(data)


    filename = OUTPUT_FOLDER / f"{data['Relationship ID']}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown)
    print(f"Created {filename.name}")

print("Finished!")