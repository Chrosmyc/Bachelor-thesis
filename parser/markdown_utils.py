from pathlib import Path
import re
import yaml


def read_md_file(file_path):
    return Path(file_path).read_text(encoding="utf-8")


def split_yaml_and_markdown(content):
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)

    if not match:
        raise ValueError("No valid YAML frontmatter found.")

    yaml_text = match.group(1)
    markdown_text = match.group(2)

    metadata = yaml.safe_load(yaml_text) or {}

    return metadata, markdown_text


def parse_sections(markdown_text):
    sections = {}
    current_heading = None
    current_lines = []

    for line in markdown_text.splitlines():
        if line.startswith("# "):
            if current_heading is not None:
                sections[current_heading] = "\n".join(current_lines).strip()

            current_heading = line.replace("# ", "", 1).strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_heading is not None:
        sections[current_heading] = "\n".join(current_lines).strip()

    return sections


def parse_list(text):
    if not text:
        return []

    result = []

    for line in text.splitlines():
        line = line.strip()

        if line.startswith("- "):
            result.append(line.replace("- ", "", 1).strip())

    if result:
        return result

    return [item.strip() for item in text.replace(";", ",").split(",") if item.strip()]


def clean_quote(text):
    return text.replace("> ", "").strip() if text else ""


def join_list(value):
    if value is None:
        return ""

    if isinstance(value, list):
        result = []

        for item in value:
            if isinstance(item, list):
                for sub_item in item:
                    result.append(str(sub_item).strip())
            else:
                result.append(str(item).strip())

        return ", ".join([item for item in result if item])

    return str(value)