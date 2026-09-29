#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from models import JDRequirements
from sources import LocalFolderSource
from matcher import evaluate

ROOT = Path(__file__).resolve().parent

def main():
    p = argparse.ArgumentParser(description="AI Recruitment Agent — offline explainable demo")
    p.add_argument("--role", default="Mobile Developer")
    p.add_argument("--openings", type=int, default=2)
    p.add_argument("--experience", default="2-4 yrs")
    p.add_argument("--skills", default="Flutter,Kotlin,REST APIs,Firebase")
    p.add_argument("--resumes", default=str(ROOT / "data" / "resumes"))
    p.add_argument("--output", default=str(ROOT / "outputs" / "candidate_evaluation.json"))
    args = p.parse_args()
    skills = [x.strip() for x in args.skills.split(",") if x.strip()]
    jd = JDRequirements(args.role, args.experience, skills, ["Git", "Agile"])
    candidates = LocalFolderSource(args.resumes).list_resumes()
    config = json.loads((ROOT / "scoring_config.json").read_text())
    ranked = evaluate(candidates, jd, config)
    payload = {
        "prototype": True,
        "source": "Local synthetic resume pool; portal labels are simulated metadata",
        "jd": {"role": args.role, "openings": args.openings, "experience": args.experience, "required_skills": skills},
        "scoring_config": config,
        "ranking": [r.to_dict() for r in ranked]
    }
    out = Path(args.output); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    report = out.with_name("candidate_ranking_report.md")
    lines = ["# Candidate Ranking Report", "", f"Role: **{args.role}**", f"Experience: **{args.experience}**", "", "| Rank | Candidate | Score | Mandatory skills | Experience |", "|---:|---|---:|---:|---:|"]
    for r in ranked:
        lines.append(f"| {r.rank} | {r.name} | {r.score}/100 | {r.breakdown['mandatorySkills']}/50 | {r.breakdown['experience']}/20 |")
    lines += ["", "## Why #1", ranked[0].reason if ranked else "No candidates processed."]
    report.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__": main()
