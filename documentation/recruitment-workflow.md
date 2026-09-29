# Recruitment Workflow

```text
Hiring Requirement
      ↓
Understand Requirement
      ↓
Generate Job Description
      ↓
Recruiter Approval
      ↓
Source Candidate Resumes
      ↓
Process / Extract Resume Data
      ↓
Compare Candidate with JD
      ↓
Calculate Explainable Score
      ↓
Rank Candidates
      ↓
Explain Top Candidate
      ↓
Recruiter Confirms Shortlist
      ↓
Prepare Interview Schedule and Drafts
```

## Prototype status

| Stage | Prototype implementation |
|---|---|
| Requirement intake | Browser form |
| JD generation | Claude when configured; deterministic fallback otherwise |
| JD approval | Recruiter checkpoint in UI |
| Resume sourcing | Local synthetic resume pool with simulated portal metadata |
| Resume parsing | Local deterministic parser |
| Candidate matching | Deterministic skill/experience/role/evidence matching |
| Ranking | Weighted deterministic scoring |
| Explanation | Generated from the score breakdown |
| Interview scheduling | Prepared slots and invitation drafts |
| External booking/email | Not performed by the prototype |

## Production path

The local source adapter can be replaced by approved ATS/job-board integrations. Calendar and email providers can replace the draft-only scheduling layer. Candidate data should be protected with authentication, authorization, audit logging, encryption, retention controls, and provider-specific compliance requirements.
