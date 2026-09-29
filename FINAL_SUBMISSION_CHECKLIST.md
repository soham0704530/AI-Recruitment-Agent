# Final Submission Checklist

## Demo

- [x] Requirement intake
- [x] Job description visible on page
- [x] Recruiter JD approval checkpoint
- [x] Resume source visible
- [x] Resume processing visible
- [x] Extracted candidate data visible
- [x] Candidate vs JD matching visible
- [x] Weighted score breakdown visible
- [x] Ranking visible
- [x] Why #1 explanation visible
- [x] Recruiter shortlist confirmation
- [x] Interview schedule and invitation drafts visible
- [x] Pipeline completion summary visible

## Evidence

- Six synthetic resumes are included under `data/resumes/`.
- Source labels are explicitly simulated.
- Numeric scoring is deterministic and configured in `scoring_config.json`.
- Candidate evaluation JSON and ranking report are included under `outputs/`.
- Tests cover resume loading, experience scoring, required-skill matching, and Java/JavaScript separation.

## Prototype boundaries

- No live Naukri/LinkedIn/Indeed scraping is claimed.
- No external email is sent.
- No external calendar meeting is booked.
- Production integrations would use approved APIs/ATS/job-board mechanisms.

## Local verification

```bash
pip install -r requirements.txt
pytest -q
python agent.py
```

Open `agent-demo.html` directly in a browser for the visual demo.
