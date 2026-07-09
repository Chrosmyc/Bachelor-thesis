from pathlib import Path
import re

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent

INPUT_FILE = SCRIPT_DIR / "Risks.txt"
OUTPUT_FOLDER = PROJECT_DIR / "data" / "risks"
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    content = f.read()

risk_blocks = re.split(r'(?=Risk ID:)', content)
risk_blocks = [block.strip() for block in risk_blocks if block.strip()]

def create_markdown(data):
    import re

    papers = [
        p.strip()
        for p in re.split(r"[,/]", data.get("Paper ID", ""))
        if p.strip()
    ]

    strategies = [
        s.strip()
        for s in re.split(r"[,/]", data.get("Modernization Strategy", ""))
        if s.strip()
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

    linked_risks = [
        r.strip()
        for r in re.split(r"[,/]", data.get("Linked Risks", ""))
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

    # --------------------------
    # YAML Header
    # --------------------------

    markdown = f"""---
id: {data.get("Risk ID","")}
type: Risk
title: {data.get("Risk Name","")}
dimension: {data.get("Dimension","")}
granularity: {data.get("Granularity Level","")}

papers:
"""

    for p in papers:
        markdown += f"  - {p}\n"

    markdown += "\nstrategy:\n"

    for s in strategies:
        markdown += f"  - {s}\n"

    markdown += "\nevidence:\n"

    for e in evidence:
        markdown += f"  - {e}\n"

    markdown += "\ntags:\n"

    for tag in tags:
        markdown += f"  - {tag}\n"

    # --------------------------
    # Markdown Inhalt
    # --------------------------

    markdown += f"""

# Description
{data.get("Risk Description","")}

# Root Cause
{data.get("Root Cause / Challenge","")}

# Trigger Event
{data.get("Trigger Event","")}

# Impact
{data.get("Impact / Consequences","")}

# Linked Risks
"""
    for risk in linked_risks:
        markdown += f"- {risk}\n"

    markdown += "\n# Stakeholders\n\n"

    for stakeholder in stakeholders:
        markdown += f"- {stakeholder}\n"

    markdown += "\n# Contextual Constraints\n\n"

    for constraint in constraints:
        markdown += f"- {constraint}\n"

    markdown += f"""

# Detection Source
{data.get("Detection Source","")}

# Standardized Risk Entry
{data.get("Standardized Risk Entry","")}

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


    filename = OUTPUT_FOLDER / f"{data['Risk ID']}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown)
    print(f"Created {filename.name}")

print("Finished!")