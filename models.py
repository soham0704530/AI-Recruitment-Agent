from dataclasses import dataclass, asdict
from typing import List, Dict, Any

@dataclass
class ParsedResume:
    id: str
    name: str
    source: str
    source_type: str
    resume_file: str
    headline: str
    experience: float
    skills: List[str]
    education: str
    roles: List[str]
    projects: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class JDRequirements:
    role: str
    experience: str
    required_skills: List[str]
    preferred_skills: List[str]

@dataclass
class CandidateEvaluation:
    candidate_id: str
    name: str
    score: int
    breakdown: Dict[str, int]
    matched_skills: List[str]
    missing_skills: List[str]
    preferred_matched: List[str]
    experience_fit: str
    reason: str
    rank: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
