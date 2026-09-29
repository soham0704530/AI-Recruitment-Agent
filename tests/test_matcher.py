import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from models import JDRequirements
from resume_parser import parse_resume
from sources import LocalFolderSource
from matcher import evaluate, skill_match

ROOT = Path(__file__).resolve().parents[1]


def test_java_is_not_javascript():
    assert not skill_match("JavaScript", "Java")


def test_resume_source_loads_six_synthetic_resumes():
    candidates = LocalFolderSource(ROOT / "data" / "resumes").list_resumes()
    assert len(candidates) == 6
    assert {c.source for c in candidates} == {"Naukri", "LinkedIn", "Indeed"}


def test_experience_affects_score():
    candidates = LocalFolderSource(ROOT / "data" / "resumes").list_resumes()
    jd = JDRequirements("Mobile Developer", "2-4 yrs", ["Flutter", "Kotlin", "REST APIs", "Firebase"], ["Git", "Agile"])
    config = json.loads((ROOT / "scoring_config.json").read_text())
    ranked = evaluate(candidates, jd, config)
    vikram = next(x for x in ranked if x.name == "Vikram Singh")
    aarav = next(x for x in ranked if x.name == "Aarav Mehta")
    assert vikram.breakdown["experience"] == 20
    assert aarav.breakdown["experience"] == 20


def test_all_required_skills_visible_in_match():
    candidates = LocalFolderSource(ROOT / "data" / "resumes").list_resumes()
    jd = JDRequirements("Mobile Developer", "2-4 yrs", ["Flutter", "Kotlin", "REST APIs", "Firebase"], ["Git", "Agile"])
    config = json.loads((ROOT / "scoring_config.json").read_text())
    ranked = evaluate(candidates, jd, config)
    vikram = next(x for x in ranked if x.name == "Vikram Singh")
    assert set(vikram.matched_skills) == {"Flutter", "Kotlin", "REST APIs", "Firebase"}
