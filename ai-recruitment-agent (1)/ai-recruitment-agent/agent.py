"""
AI Recruitment Agent
=====================
A minimal, readable reference implementation of the agent described in
README.md. It takes a hiring requirement, drafts a job description with
Claude, "sources" candidates from a local mock pool (stand-in for
Naukri.com / LinkedIn / Indeed), ranks them against the JD with Claude,
and drafts an interview invitation for the top candidate.

Run:
    export ANTHROPIC_API_KEY=sk-ant-...
    python agent.py --role "Mobile Developer" --openings 2 \
        --skills "Flutter,Kotlin,REST APIs,Firebase" --experience "Mid (2-4 yrs)"
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from typing import List

import anthropic

MODEL = "claude-sonnet-4-6"

# ---------------------------------------------------------------------------
# Mock candidate pool — stands in for real Naukri.com / LinkedIn / Indeed
# API integrations, which require paid recruiter access and are outside the
# scope of this demo. Swap `source_candidates()` for real API calls to go
# to production.
# ---------------------------------------------------------------------------
CANDIDATE_POOL = [
    {"id": "C-104", "name": "Aarav Mehta", "headline": "Flutter Developer, 3 yrs - e-commerce apps",
     "skills": ["Flutter", "Dart", "Firebase", "REST APIs", "CI/CD"], "exp": 3, "platform": "LinkedIn"},
    {"id": "C-118", "name": "Priya Nair", "headline": "Android Engineer, 4 yrs - fintech",
     "skills": ["Kotlin", "Android SDK", "REST APIs", "Room DB"], "exp": 4, "platform": "Naukri.com"},
    {"id": "C-127", "name": "Rohan Iyer", "headline": "iOS Developer, 2 yrs - healthtech",
     "skills": ["Swift", "SwiftUI", "REST APIs", "Core Data"], "exp": 2, "platform": "Indeed"},
    {"id": "C-133", "name": "Sneha Kulkarni", "headline": "React Native Developer, 3 yrs",
     "skills": ["React Native", "JavaScript", "Firebase", "Redux"], "exp": 3, "platform": "LinkedIn"},
    {"id": "C-142", "name": "Vikram Singh", "headline": "Cross-platform Mobile Dev, 5 yrs",
     "skills": ["Flutter", "Kotlin", "Firebase", "REST APIs", "GraphQL"], "exp": 5, "platform": "Naukri.com"},
    {"id": "C-151", "name": "Ananya Rao", "headline": "Business Analyst, 3 yrs - SaaS",
     "skills": ["Requirement Gathering", "SQL", "Jira", "Stakeholder Management", "Agile"], "exp": 3, "platform": "LinkedIn"},
    {"id": "C-159", "name": "Karan Patel", "headline": "Business Analyst, 5 yrs - banking domain",
     "skills": ["SQL", "BRD/FRD", "Stakeholder Management", "Power BI", "Agile"], "exp": 5, "platform": "Naukri.com"},
    {"id": "C-166", "name": "Divya Menon", "headline": "Junior Business Analyst, 1 yr",
     "skills": ["Excel", "SQL", "Documentation", "Agile"], "exp": 1, "platform": "Indeed"},
    {"id": "C-171", "name": "Farhan Sheikh", "headline": "Flutter Developer, 1.5 yrs",
     "skills": ["Flutter", "Dart", "REST APIs"], "exp": 1.5, "platform": "Naukri.com"},
    {"id": "C-180", "name": "Meera Joshi", "headline": "Mobile QA turned Android Dev, 2 yrs",
     "skills": ["Kotlin", "Android SDK", "Testing", "REST APIs"], "exp": 2, "platform": "LinkedIn"},
    {"id": "C-188", "name": "Aditya Kapoor", "headline": "Senior Mobile Architect, 7 yrs",
     "skills": ["Flutter", "Kotlin", "Swift", "System Design", "REST APIs"], "exp": 7, "platform": "LinkedIn"},
    {"id": "C-193", "name": "Ishita Bose", "headline": "Product/Business Analyst, 4 yrs",
     "skills": ["Stakeholder Management", "SQL", "Wireframing", "Agile", "Jira"], "exp": 4, "platform": "Indeed"},
]


@dataclass
class Requirement:
    role: str
    openings: int
    skills: List[str]
    experience: str


@dataclass
class JobDescription:
    title: str
    summary: str
    responsibilities: List[str]
    required_skills: List[str]
    nice_to_have: List[str] = field(default_factory=list)
    employment_type: str = "Full-time"
    location: str = "India"


def get_client() -> anthropic.Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit("Set ANTHROPIC_API_KEY before running (see README.md).")
    return anthropic.Anthropic(api_key=api_key)


def extract_json(text: str):
    match = re.search(r"\{[\s\S]*\}|\[[\s\S]*\]", text)
    if not match:
        raise ValueError("No JSON object/array found in model output")
    return json.loads(match.group(0))


# ---------------------------------------------------------------------------
# Step 2: Generate the job description
# ---------------------------------------------------------------------------
def generate_jd(client: anthropic.Anthropic, req: Requirement, company: str) -> JobDescription:
    prompt = (
        f'Write a job description as JSON only (no markdown, no prose outside the JSON) '
        f'for the role "{req.role}" at an IT services company called {company}. '
        f'Openings: {req.openings}. Experience level: {req.experience}. '
        f'Key skills: {", ".join(req.skills)}. '
        'Return this exact JSON shape: {"title": string, "summary": string, '
        '"responsibilities": string[4-6], "requiredSkills": string[4-7], '
        '"niceToHave": string[2-3], "employmentType": string, "location": string}. '
        'Keep every item concise (under 18 words).'
    )
    resp = client.messages.create(model=MODEL, max_tokens=1000,
                                   messages=[{"role": "user", "content": prompt}])
    data = extract_json(resp.content[0].text)
    return JobDescription(
        title=data["title"], summary=data["summary"],
        responsibilities=data["responsibilities"], required_skills=data["requiredSkills"],
        nice_to_have=data.get("niceToHave", []),
        employment_type=data.get("employmentType", "Full-time"),
        location=data.get("location", "India"),
    )


# ---------------------------------------------------------------------------
# Step 4: Source candidates (mock — replace with real portal APIs)
# ---------------------------------------------------------------------------
def source_candidates(req: Requirement, pool=CANDIDATE_POOL, limit: int = 6):
    req_skills = [s.lower() for s in req.skills]

    def hit_count(cand):
        return sum(1 for sk in cand["skills"]
                   if any(rs in sk.lower() or sk.lower() in rs for rs in req_skills))

    scored = [(c, hit_count(c)) for c in pool]
    scored = [c for c, h in scored if h > 0]
    scored.sort(key=lambda c: hit_count(c), reverse=True)
    return scored[:limit]


# ---------------------------------------------------------------------------
# Step 5: AI shortlisting / ranking
# ---------------------------------------------------------------------------
def rank_candidates(client: anthropic.Anthropic, jd: JobDescription, candidates):
    payload = [{"id": c["id"], "headline": c["headline"], "skills": c["skills"], "exp": c["exp"]}
               for c in candidates]
    prompt = (
        f"Job description: {jd.title}. Required skills: {', '.join(jd.required_skills)}. "
        f"Candidates (JSON): {json.dumps(payload)}. "
        'Score each candidate 0-100 for fit against the JD and give a one-sentence reason. '
        'Return ONLY a JSON array like [{"id":"C-104","score":87,"reason":"..."}], '
        "sorted by score descending, same length as input."
    )
    resp = client.messages.create(model=MODEL, max_tokens=1000,
                                   messages=[{"role": "user", "content": prompt}])
    scores = extract_json(resp.content[0].text)
    by_id = {c["id"]: c for c in candidates}
    ranked = []
    for s in scores:
        c = by_id.get(s["id"])
        if c:
            ranked.append({**c, "score": s["score"], "reason": s["reason"]})
    ranked.sort(key=lambda c: c["score"], reverse=True)
    return ranked


# ---------------------------------------------------------------------------
# Step 7: Draft interview invitation for the top candidate
# ---------------------------------------------------------------------------
def draft_invitation(client: anthropic.Anthropic, jd: JobDescription, candidate, company: str, slot: str) -> str:
    prompt = (
        f"Write a short, warm interview invitation email (under 90 words) to {candidate['name']} "
        f"for the \"{jd.title}\" role at {company}, proposing a telephonic interview on {slot}. "
        "Plain text only."
    )
    resp = client.messages.create(model=MODEL, max_tokens=300,
                                   messages=[{"role": "user", "content": prompt}])
    return resp.content[0].text.strip()


def run(req: Requirement, company: str = "Technical Pots IT Solutions"):
    client = get_client()

    print(f"\n[1/5] Understanding requirement: {req.role} x{req.openings} ({req.experience})")
    print(f"      Skills: {', '.join(req.skills)}")

    print("\n[2/5] Generating job description...")
    jd = generate_jd(client, req, company)
    print(f"      Title: {jd.title}")
    print(f"      Summary: {jd.summary}")
    for r in jd.responsibilities:
        print(f"        - {r}")

    print("\n[3/5] Sourcing candidates from Naukri.com, LinkedIn, Indeed (mock pool)...")
    sourced = source_candidates(req)
    for c in sourced:
        print(f"      {c['id']}  {c['name']:<16} [{c['platform']}]  {c['headline']}")

    print("\n[4/5] Ranking candidates against the JD...")
    ranked = rank_candidates(client, jd, sourced)
    for i, c in enumerate(ranked, 1):
        print(f"      #{i} {c['name']:<16} score={c['score']:<4} {c['reason']}")

    if ranked:
        print("\n[5/5] Scheduling interview with top candidate...")
        top = ranked[0]
        slot = "Thursday 11:00 AM IST"
        email = draft_invitation(client, jd, top, company, slot)
        print(f"      To: {top['name']}  |  Slot: {slot}")
        print("      ---")
        print("      " + email.replace("\n", "\n      "))

    print("\nDone.")


def main():
    parser = argparse.ArgumentParser(description="Run the AI Recruitment Agent.")
    parser.add_argument("--role", required=True)
    parser.add_argument("--openings", type=int, default=1)
    parser.add_argument("--skills", required=True, help="Comma-separated list")
    parser.add_argument("--experience", default="Mid (2-4 yrs)")
    parser.add_argument("--company", default="Technical Pots IT Solutions")
    args = parser.parse_args()

    req = Requirement(
        role=args.role, openings=args.openings,
        skills=[s.strip() for s in args.skills.split(",") if s.strip()],
        experience=args.experience,
    )
    run(req, company=args.company)


if __name__ == "__main__":
    main()
