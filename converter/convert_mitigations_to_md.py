from pathlib import Path
import re

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent

INPUT_FILE = SCRIPT_DIR / "Mitigations.txt"
OUTPUT_FOLDER = PROJECT_DIR / "data" / "mitigations"
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


with open(INPUT_FILE, "r", encoding="utf-8") as f:
    content = f.read()

risk_blocks = re.split(r'(?=Mitigation ID:)', content)
risk_blocks = [block.strip() for block in risk_blocks if block.strip()]

def create_markdown(data):
    import re

    papers = [
        p.strip()
        for p in re.split(r"[,/]", data.get("Paper ID", ""))
        if p.strip()
    ]

    related_risks = [
        r.strip()
        for r in re.split(r"[,/]", data.get("Related Risks", ""))
        if r.strip()
    ]

    stakeholders = [
        s.strip()
        for s in data.get("Stakeholders", "").split(",")
        if s.strip()
    ]

    constraints = [
        c.strip()
        for c in data.get("Contextual Constraints", "").split(",")
        if c.strip()
    ]

    evidence = [
        e.strip()
        for e in re.split(r"[,/]", data.get("Evidence Type", ""))
        if e.strip()
    ]

    tags = [
        t.strip().replace("#", "")
        for t in re.split(r"[,/]", data.get("Key Terminology (Tags)", ""))
        if t.strip()
    ]

    markdown = f"""---
id: {data.get("Mitigation ID","")}
type: Mitigation
title: {data.get("Mitigation Name","")}

papers:
"""

    for p in papers:
        markdown += f"  - {p}\n"

    markdown += f"""
strategy_type: {data.get("Strategy Type","")}
probability_of_success: {data.get("Probability of Success","")}
effort: {data.get("Effort of Mitigation","")}

evidence:
"""

    for e in evidence:
        markdown += f"  - {e}\n"

    markdown += "\ntags:\n"

    for tag in tags:
        markdown += f"  - {tag}\n"

    markdown += "\nrelated_risks:\n"

    for risk in related_risks:
        markdown += f"  - {risk}\n"

    markdown += f"""

# Description
{data.get("Mitigation Description","")}

# Prerequisites
{data.get("Prerequisites","")}

# Tools / Technologies
{data.get("Tools / Technologies","")}

# Trade-offs / Side Effects
{data.get("Trade-offs / Side Effects","")}

# Effectiveness
{data.get("Effectiveness","")}

# Stakeholders
"""

    for stakeholder in stakeholders:
        markdown += f"- {stakeholder}\n"

    markdown += "\n# Contextual Constraints\n\n"

    for constraint in constraints:
        markdown += f"- {constraint}\n"

    markdown += f"""

# Standardized Mitigation Entry
{data.get("Standardized Mitigation Entry","")}

# Key Quote for Prompting
> {data.get("Key Quote for Prompting","")}

# Logic Pattern
{data.get("Logic Pattern","")}
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


    filename = OUTPUT_FOLDER / f"{data['Mitigation ID']}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown)
    print(f"Created {filename.name}")
    
print("Finished!")