# AI Recruitment Agent

An autonomous agent that takes a hiring requirement and runs the recruitment
pipeline end-to-end: understands the role, drafts a job description, sources
candidates across job platforms, ranks them against the JD, and schedules
interviews — with a human approval checkpoint after JD generation and after
shortlisting.

Built for an "AI Agents" assignment, based on a real use case described by
**Technical Pots IT Solutions** ([tpots.co](https://tpots.co/)).

🎥 **Demo video:** _add your link here after recording (see "Recording a demo" below)_
🔗 **Live interactive demo:** `agent-demo.html` in this repo — open it directly in a browser (see below)

## What the agent does

```
Requirement  ──▶  Understand role   ──▶  Generate JD   ──▶  [Recruiter approves]
                                                                    │
                                                                    ▼
Schedule interviews  ◀──  [Recruiter confirms]  ◀──  Rank candidates  ◀──  Source candidates
                                                                            (Naukri / LinkedIn / Indeed)
```

| Step | Action | How |
|---|---|---|
| 1 | Understand requirement | Parses role, headcount, skills, seniority into a structured brief |
| 2 | Generate JD | Claude drafts a JD in the company's format (JSON → rendered) |
| 3 | **Human checkpoint** | Recruiter approves the JD before it goes out |
| 4 | Source candidates | Searches a candidate pool (stand-in for Naukri.com / LinkedIn / Indeed APIs) |
| 5 | AI shortlisting | Claude scores every sourced profile 0–100 against the JD, with reasoning |
| 6 | **Human checkpoint** | Recruiter confirms the shortlist |
| 7 | Schedule interviews | Proposes slots and drafts an interview invitation for the top candidate |

## Two ways to run it

### 1. Interactive browser demo (`agent-demo.html`)

A single self-contained HTML file — open it in any browser (double-click it,
or `python3 -m http.server` and visit the page). It calls the Claude API
directly from the browser to generate the JD and rank candidates, and walks
through the pipeline step by step with a live status log. This is the
easiest way to **record a demo video**.

This file was originally built as a Claude.ai Artifact, where API calls are
proxied automatically with no key needed. To run it standalone (outside
Claude.ai — e.g. after cloning this repo), paste your own key into the
**Anthropic API key** field at the top of the page before clicking **Run
agent**. The key is only held in browser memory for that session — it is
never written to disk, localStorage, or sent anywhere except
`api.anthropic.com`. Get a key from the
[Anthropic Console](https://console.anthropic.com/settings/keys).

> Calling the API directly from a browser normally hits a CORS block; this
> file sends the `anthropic-dangerous-direct-browser-access` header to allow
> it. That header is intended for local testing/demos like this one — for a
> real product, calls should go through a backend so the key is never
> exposed client-side.

### 2. Python CLI (`agent.py`)

```bash
pip install -r requirements.txt
cp .env.example .env        # then add your ANTHROPIC_API_KEY
export ANTHROPIC_API_KEY=sk-ant-...

python agent.py \
  --role "Mobile Developer" \
  --openings 2 \
  --skills "Flutter,Kotlin,REST APIs,Firebase" \
  --experience "Mid (2-4 yrs)"
```

Example output:

```
[1/5] Understanding requirement: Mobile Developer x2 (Mid (2-4 yrs))
      Skills: Flutter, Kotlin, REST APIs, Firebase

[2/5] Generating job description...
      Title: Mobile Developer
      Summary: We're looking for a Mobile Developer to build cross-platform apps...
        - Design and build Flutter/Kotlin mobile applications
        - Integrate REST APIs and Firebase services
        ...

[3/5] Sourcing candidates from Naukri.com, LinkedIn, Indeed (mock pool)...
      C-142  Vikram Singh     [Naukri.com]  Cross-platform Mobile Dev, 5 yrs
      C-104  Aarav Mehta      [LinkedIn]    Flutter Developer, 3 yrs - e-commerce apps
      ...

[4/5] Ranking candidates against the JD...
      #1 Vikram Singh     score=92   Strong match on Flutter, Kotlin and REST APIs with 5 yrs experience.
      #2 Aarav Mehta      score=85   Direct Flutter/Firebase match, slightly less overall experience.
      ...

[5/5] Scheduling interview with top candidate...
      To: Vikram Singh  |  Slot: Thursday 11:00 AM IST
      ---
      Hi Vikram, thanks for your profile for the Mobile Developer role...
```

## Architecture

- **Orchestrator** — the `run()` function in `agent.py` (or the pipeline
  runner in `agent-demo.html`) sequences the steps and pauses at the two
  human-in-the-loop checkpoints.
- **LLM reasoning** — Claude (`claude-sonnet-4-6`) is used for two
  judgment-heavy tasks: drafting the JD and scoring/ranking candidates.
  Both are prompted to return structured JSON so the output can be rendered
  or processed programmatically.
- **Sourcing** — `source_candidates()` currently reads from a local mock
  pool (`CANDIDATE_POOL`) that stands in for real Naukri.com / LinkedIn /
  Indeed recruiter APIs, which require paid access and partnership
  agreements outside the scope of this demo. Swap this function for real
  API calls to go to production — the rest of the pipeline is unchanged.
- **Human-in-the-loop** — the agent does not auto-publish a JD or
  auto-contact candidates; it stops and waits for explicit approval at two
  points, matching how the interviewed stakeholder described the process.

## Why the platform integrations are mocked

Naukri.com, LinkedIn and Indeed all require paid recruiter accounts, signed
API agreements, and in some cases company verification before granting
programmatic access to candidate search. For this assignment, sourcing is
simulated with a small local candidate pool so the full pipeline (JD →
source → rank → schedule) can be demonstrated end-to-end. `source_candidates()`
is intentionally isolated so it can be replaced with real API calls without
touching any other part of the agent.

## Recording a demo

1. Open `agent-demo.html` in a browser.
2. Start screen recording (OBS, Loom, or your OS's built-in recorder).
3. Fill in a role (e.g. "Business Analyst" or "Mobile Developer"), openings,
   and skills, then click **Run agent**.
4. Narrate each step as it completes: requirement parsing → JD draft →
   approve → sourcing → AI shortlisting → approve → scheduling.
5. Export the recording and upload it (YouTube "unlisted" or Google Drive
   with link sharing works well for assignment submissions).

## Project structure

```
ai-recruitment-agent/
├── agent.py            # Python CLI implementation
├── agent-demo.html      # Interactive browser demo (for the video)
├── requirements.txt
├── .env.example
└── README.md
```

## Pushing this to GitHub

```bash
cd ai-recruitment-agent
git init
git add .
git commit -m "AI Recruitment Agent"
git branch -M main
git remote add origin https://github.com/<your-username>/ai-recruitment-agent.git
git push -u origin main
```
