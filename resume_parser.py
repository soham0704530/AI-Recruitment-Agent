from pathlib import Path
import re
from models import ParsedResume

HEADER_RE = re.compile(r"^([^:]+):\s*(.*)$")

def _lines(text):
    return [x.strip() for x in text.splitlines() if x.strip()]

def _field(lines, key, default=""):
    prefix = key.lower() + ":"
    for line in lines:
        if line.lower().startswith(prefix):
            return line[len(prefix):].strip()
    return default

def _list_field(lines, key):
    value = _field(lines, key, "")
    return [x.strip() for x in value.split(",") if x.strip()]

def parse_resume(path: Path):
    text = path.read_text(encoding="utf-8")
    lines = _lines(text)
    exp_raw = _field(lines, "Experience", "0")
    m = re.search(r"(\d+(?:\.\d+)?)", exp_raw)
    experience = float(m.group(1)) if m else 0.0
    projects = []
    in_projects = False
    for line in lines:
        if line.lower() == "projects:":
            in_projects = True
            continue
        if in_projects:
            if line.startswith("-"):
                projects.append(line[1:].strip())
            elif ":" in line and not line.startswith("-"):
                in_projects = False
    # Source metadata is intentionally synthetic and stored in the resume header.
    return ParsedResume(
        id=_field(lines, "ID", path.stem),
        name=_field(lines, "Name", path.stem.replace("-", " ").title()),
        source=_field(lines, "Source", "LocalDemo"),
        source_type=_field(lines, "SourceType", "Synthetic Demo"),
        resume_file=path.name,
        headline=_field(lines, "Headline", ""),
        experience=experience,
        skills=_list_field(lines, "Skills"),
        education=_field(lines, "Education", "Not specified"),
        roles=_list_field(lines, "Roles"),
        projects=projects,
    )
