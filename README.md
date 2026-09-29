# AI Recruitment Agent

A prototype recruitment workflow for Technical Pots IT Solutions (TPots).

## Demo flow

Hiring requirement → JD generation → recruiter approval → resume source → resume processing → candidate/JD matching → deterministic scoring → ranking → why #1 → recruiter shortlist confirmation → interview preparation.

## What the demo shows

The browser demo keeps the outputs visible on the same page so a reviewer can inspect the workflow instead of only seeing progress indicators.

- Job Description generated from hiring requirements
- Six synthetic resumes and simulated source metadata
- Resume processing and extracted candidate fields
- Candidate-vs-JD skill and experience comparison
- Explainable weighted score breakdown
- Complete candidate ranking
- Score arithmetic and selection reasoning
- Why the top candidate ranked first
- Recruiter shortlist checkpoint
- Interview slots and invitation drafts
- Final pipeline summary

## Resume sourcing

The browser demo uses six synthetic resumes in `data/resumes/`. Each candidate has simulated source metadata for Naukri, LinkedIn or Indeed. This is intentionally not presented as live scraping.

The Python source layer contains a real local-folder adapter plus placeholders for approved production integrations.

## Explainable scoring

The final candidate score is calculated by application logic:

- Mandatory skills: 50%
- Experience fit: 20%
- Preferred skills: 10%
- Role relevance: 10%
- Relevant evidence: 10%

The UI shows component scores, matched/missing skills, extracted profile evidence, score arithmetic, and the margin between #1 and #2.

## Architecture

```text
Recruiter Requirement
        ↓
Requirement / JD Understanding
        ↓
Job Description
        ↓
Recruiter Approval
        ↓
Resume Source Adapter
        ↓
Resume Parser
        ↓
Structured Candidate Data
        ↓
JD ↔ Candidate Matching
        ↓
Deterministic Scoring Engine
        ↓
Ranking + Explanation
        ↓
Recruiter Shortlist Approval
        ↓
Interview Preparation
```

The LLM is used where language understanding is useful. The application controls structured business rules, numerical scoring, ranking, and recruiter checkpoints.

## Run the browser demo

Open `agent-demo.html` directly in a browser. The demo works without an API key using local deterministic fallbacks. If an Anthropic API key is supplied, Claude can be used for JD generation and invitation wording.

## Run the Python evaluation

```bash
pip install -r requirements.txt
python agent.py
```

## Test

```bash
pytest -q
```

## Outputs

- `outputs/candidate_evaluation.json` — structured candidate evaluation
- `outputs/candidate_ranking_report.md` — human-readable ranking report

## Documentation

- `documentation/recruitment-workflow.md` — workflow and prototype status
- `documentation/candidate-selection-explained.md` — scoring and ranking walkthrough
- `documentation/voiceover_script.txt` — demo narration
- `FINAL_SUBMISSION_CHECKLIST.md` — submission verification checklist
- `SUBMISSION_MESSAGE.txt` — suggested message to the evaluator

## Prototype boundaries

Naukri/LinkedIn/Indeed are simulated sources. Interview slots and invitation text are prepared for recruiter review; no external meeting is booked and no email is sent. Production would use approved ATS/job-board integrations and calendar/email providers.
