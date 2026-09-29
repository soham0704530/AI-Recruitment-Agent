import json
import re
from pathlib import Path
from models import JDRequirements, CandidateEvaluation


def norm(v):
    return re.sub(r"[^a-z0-9+#.]+", " ", str(v).lower().replace("apis", "api")).strip()

ALIASES = {
    "rest api": {"rest api", "rest apis", "restful api", "restful apis", "api integration"},
    "firebase": {"firebase", "firebase auth", "firebase authentication"},
    "flutter": {"flutter", "flutter framework"},
}

def skill_match(a, b):
    a, b = norm(a), norm(b)
    if not a or not b:
        return False
    if a == b:
        return True
    for canonical, vals in ALIASES.items():
        if a in vals and b in vals:
            return True
    return False

def parse_range(text):
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:-|–|to)\s*(\d+(?:\.\d+)?)", str(text), re.I)
    if m:
        return float(m.group(1)), float(m.group(2))
    m = re.search(r"(\d+(?:\.\d+)?)", str(text))
    x = float(m.group(1)) if m else 0
    return x, x

def experience_score(years, text, max_points=20):
    lo, hi = parse_range(text)
    if lo <= years <= hi:
        return max_points
    if years < lo:
        return round(max(0, max_points * years / max(lo, 1)), 2)
    over = years - hi
    return round(max(8, max_points - over * 4), 2)

def role_score(candidate, role):
    r = norm(role)
    roles = [norm(x) for x in candidate.roles]
    if r in roles:
        return 10
    words = [w for w in r.split() if len(w) > 2]
    overlap = sum(any(w in rr for rr in roles) for w in words)
    if overlap >= 2: return 9
    if overlap == 1: return 6
    if "mobile" in r and any(norm(s) in {"flutter", "kotlin", "swift", "react native"} for s in candidate.skills):
        return 5
    return 2

def evaluate(candidates, jd: JDRequirements, config):
    w = config["weights"]
    results = []
    lo, hi = parse_range(jd.experience)
    for c in candidates:
        matched = [req for req in jd.required_skills if any(skill_match(s, req) for s in c.skills)]
        missing = [req for req in jd.required_skills if req not in matched]
        pref = [req for req in jd.preferred_skills if any(skill_match(s, req) for s in c.skills)]
        mandatory = w["mandatory_skills"] * (len(matched) / len(jd.required_skills)) if jd.required_skills else w["mandatory_skills"]
        exp = experience_score(c.experience, jd.experience, w["experience_fit"])
        pref_score = w["preferred_skills"] * (len(pref) / len(jd.preferred_skills)) if jd.preferred_skills else 0
        role = role_score(c, jd.role)
        evidence_hits = sum(any(norm(req) in norm(p) for req in jd.required_skills) for p in c.projects)
        evidence = min(w["evidence"], 10 if evidence_hits >= 2 else 7 if evidence_hits == 1 else 3)
        score = round(mandatory + exp + pref_score + role + evidence)
        fit = "within requested range" if lo <= c.experience <= hi else "outside requested range"
        reason = f"{len(matched)}/{len(jd.required_skills)} mandatory skills matched; experience is {fit}; {len(pref)} preferred skill(s) matched."
        results.append(CandidateEvaluation(c.id, c.name, score, {
            "mandatorySkills": round(mandatory), "experience": round(exp), "preferredSkills": round(pref_score),
            "roleRelevance": round(role), "evidence": round(evidence)
        }, matched, missing, pref, fit, reason))
    results.sort(key=lambda x: (-x.score, -len(x.matched_skills), abs(((lo + hi) / 2) - next(c.experience for c in candidates if c.id == x.candidate_id)), -len(x.preferred_matched), x.candidate_id))
    for i, r in enumerate(results, 1): r.rank = i
    return results
