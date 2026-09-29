# Candidate Selection Explained

## Demo role

- Role: Mobile Developer
- Openings: 2
- Experience target: 2–4 years
- Required skills: Flutter, Kotlin, REST APIs, Firebase
- Preferred skills: Git, Agile

## Resume source

The browser prototype loads six synthetic resume files from `data/resumes/`. Each file contains source metadata labelled Naukri, LinkedIn, or Indeed. These are simulated source labels, not live scraping.

Production connectors are represented by adapter classes in `sources.py` and would be replaced by approved ATS/job-board integrations.

## Processing

Each resume is parsed into structured fields:

- Candidate name
- Experience
- Skills
- Education
- Previous roles
- Project evidence
- Resume filename
- Source metadata

## Matching and scoring

The application compares every candidate against the same approved JD.

| Criterion | Weight |
|---|---:|
| Mandatory skills | 50 |
| Experience fit | 20 |
| Preferred skills | 10 |
| Role relevance | 10 |
| Relevant evidence | 10 |
| **Total** | **100** |

The numeric score is calculated by deterministic application code. The LLM may assist with language generation, but it does not arbitrarily assign the final score.

## Experience handling

The 2–4 year band is treated as a scoring factor rather than an automatic rejection. Candidates outside the band can receive a reduced experience-fit score while remaining visible to the recruiter.

## Ranking

Candidates are sorted by total score. Tie-breaking uses required-skill coverage, experience distance to the band midpoint, preferred-skill coverage, and candidate ID.

## Why the top candidate is shown

The browser UI generates the explanation from the same score breakdown used for ranking. It also shows the score gap between candidate #1 and candidate #2.

This makes the result auditable: a recruiter can inspect the matched skills, missing skills, experience fit, score components, and resume evidence before confirming the shortlist.
