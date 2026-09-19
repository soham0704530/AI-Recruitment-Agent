# AI Recruitment Agent — Workflow Documentation

## 1. Purpose
This prototype demonstrates: **Hiring Requirement → Requirement Understanding → JD Generation → Platform Sourcing → Profile Processing → Candidate Matching → Shortlisting → Interview Scheduling**

## 2. Demonstration Hiring Requirement
- **Role:** Mobile Developer
- **Openings:** 2
- **Experience:** Mid-level (2–4 years)
- **Required Skills:** Flutter, Kotlin, REST APIs, Firebase
- **Target Applications:** 6

## 3. Job Description Generation
The agent converts the hiring requirement into structured data and generates a standard JD containing the role summary, responsibilities, required skills, qualifications, nice-to-have skills, employment details and culture/benefits.

**Generated attachment:** `outputs/Mobile_Developer_JD.pdf`

The browser prototype supports an external LLM integration when configured. If that integration is unavailable, the application uses a deterministic local fallback so the workflow remains demonstrable. The fallback should not be represented as an external LLM response.

## 4. Platform Sourcing
The prototype demonstrates sourcing adapters/logical steps for Naukri, LinkedIn and Indeed. For this prototype, platform results are represented by structured demonstration candidate records rather than private/live scraping of candidate databases.

```text
Approved JD → Platform Search Criteria → Naukri / LinkedIn / Indeed → Candidate Profiles → Normalized Candidate Records
```

## 5. Candidate Profile Processing
Candidate records contain fields such as name, headline, platform/source, experience and skills.

```text
Candidate Profile → Extract / Normalize Fields → Normalize Skills → Compare Against JD → Calculate Match → Rank Candidates
```

In the current prototype, candidate records are processed locally/in memory. A production implementation could persist raw files in object storage and structured records in a database.

## 6. Candidate Matching Logic
The local fallback ranking logic uses the number of direct requested-skill matches:

```javascript
score: Math.min(96, 55 + c.hits * 10)
```

and records the explanation:

```javascript
reason: c.hits + ' of the requested skills matched directly.'
```

A production implementation could add weighted matching for required skills, experience, role relevance, location/work mode, qualifications and nice-to-have skills.

## 7. Vikram Singh — Selection Example
The demonstration compares Vikram Singh against the approved JD:

| JD requirement | Candidate match |
|---|---|
| Flutter | ✓ |
| Kotlin | ✓ |
| REST APIs | ✓ |
| Firebase | ✓ |
| 2–4 years experience | ✓ |

The system records the direct skill-match count, calculates the match score using the configured local logic, and ranks candidates accordingly.

**Prototype note:** when the external LLM ranking call is unavailable, this result is a local/rule-based matching result.

## 8. Shortlist Output
The shortlist displays candidate rank, name, headline, source, experience, skills, match score and evaluation reasoning.

## 9. Interview Scheduling
After ranking, the prototype prepares proposed interview slots and an invitation message for recruiter review. It should be described as preparing proposed slots, not booking a real calendar meeting unless a calendar integration is connected.

## 10. Storage / Output Locations
### Current prototype
- Generated JD: `outputs/Mobile_Developer_JD.pdf`
- Candidate records: structured local/in-memory prototype data
- Matching results: generated during the workflow
- Interview schedule/invitation: generated in the demo workflow

### Production extension
```text
Object Storage
├── resumes/
├── generated-jds/
└── interview-documents/

Database
├── hiring_requirements
├── job_descriptions
├── candidates
├── candidate_matches
└── interviews
```

## 11. End-to-End Workflow
```text
Hiring Requirement
        ↓
Requirement Normalization
        ↓
JD Generation
        ↓
Recruiter Approval
        ↓
Platform Sourcing
        ↓
Candidate Profile Collection
        ↓
Profile Normalization
        ↓
JD / Candidate Matching
        ↓
Candidate Ranking
        ↓
Shortlist
        ↓
Interview Slot Preparation
        ↓
Interview Invitation
        ↓
Recruiter Review
```

## 12. Prototype vs Production
| Area | Current Prototype | Production Extension |
|---|---|---|
| JD generation | LLM integration + local fallback | Server-side LLM integration |
| Platform sourcing | Demonstration adapters/data | Approved platform APIs/integrations |
| Candidate processing | Local structured records | Resume/profile ingestion pipeline |
| Matching | Transparent local skill matching fallback | Weighted/LLM-assisted matching |
| Storage | Local/in-memory demo data + PDF output | PostgreSQL + object storage |
| Scheduling | Proposed slots + invitation | Calendar/meeting API |
| Approval | Recruiter review in UI | RBAC + audit trail |

## 13. Video Evidence Checklist
Show: hiring requirement input; JD generation; `Mobile_Developer_JD.pdf`; platform sourcing logs; candidate structured data; matching logic; Vikram Singh's profile; skill-by-skill comparison; match score and reasoning; shortlist output; interview schedule/invitation; and project output/documentation folders.
