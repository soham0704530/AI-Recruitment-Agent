from pathlib import Path
from typing import List, Dict
from resume_parser import parse_resume

class ResumeSource:
    name = "base"
    def list_resumes(self) -> List[Dict]:
        raise NotImplementedError

class LocalFolderSource(ResumeSource):
    name = "Local synthetic resume pool"
    def __init__(self, folder):
        self.folder = Path(folder)

    def list_resumes(self) -> List[Dict]:
        items = []
        for path in sorted(self.folder.glob("*.txt")):
            items.append(parse_resume(path))
        return items

class NaukriSource(ResumeSource):
    name = "Naukri adapter (not implemented)"
    def list_resumes(self):
        raise NotImplementedError("Use an approved Naukri/ATS integration in production.")

class LinkedInSource(ResumeSource):
    name = "LinkedIn adapter (not implemented)"
    def list_resumes(self):
        raise NotImplementedError("Use an approved LinkedIn/ATS integration in production.")

class IndeedSource(ResumeSource):
    name = "Indeed adapter (not implemented)"
    def list_resumes(self):
        raise NotImplementedError("Use an approved Indeed/ATS integration in production.")
