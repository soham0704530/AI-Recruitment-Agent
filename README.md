# AI Recruitment Agent

An autonomous agent that takes a hiring requirement and runs the recruitment
pipeline end-to-end: understands the role, drafts a job description, sources
candidates across job platforms, ranks them against the JD, and schedules
interviews — with a human approval checkpoint after JD generation and after
shortlisting.

Built for an **AI Agents** assignment, based on a real hiring workflow
described by **Technical Pots IT Solutions** ([tpots.co]),
a mobile app development and web design company.

🔗 **Live interactive demo:** `agent-demo.html` in this repo — open it directly in a browser (see below)

---

## Original workflow

This agent was built against the following 7-step hiring workflow, and each
step below maps directly onto it:

1. **Requirement Intake** — role type, number of positions, number of applications to source
2. **Role Understanding** — map responsibilities, skills, and qualifications
3. **JD Creation** — role overview, responsibilities, skills, experience, culture/benefits
4. **Platform Posting** — Naukri.com, LinkedIn, and 2–3 other portals
5. **Profile Sourcing** — collect and filter candidate profiles, auto-shortlist
6. **Interview Scheduling** — sync calendars, notify candidates and HR
7. **End-to-End Flow** — continuous loop: intake → JD → posting → sourcing → shortlisting → scheduling

## What the agent does

```
Requirement  ──▶  Understand role   ──▶  Generate JD   ──▶  [Recruiter approves]
                                                                    │
                                                                    ▼
Schedule interviews  ◀──  [Recruiter confirms]  ◀──  Rank candidates  ◀──  Source candidates
                                                                            (Naukri / LinkedIn / Indeed)
```

| # | Workflow step | What the agent does |
|---|---|---|
| 1 | Requirement Intake | Takes role, headcount, required skills, and seniority as input |
| 2 | Role Understanding | Parses the input into a structured brief (skills, seniority, responsibilities) |
| 3 | JD Creation | Claude drafts a full JD (overview, responsibilities, required + nice-to-have skills, employment type, location) |
| — | **Human checkpoint** | Recruiter approves the JD before it goes further |
| 4 | Platform Posting | Simulated posting to Naukri.com, LinkedIn, and Indeed |
| 5 | Profile Sourcing & Shortlisting | Sources candidate profiles, filters against JD criteria, Claude scores each 0–100 with reasoning |
| — | **Human checkpoint** | Recruiter confirms the shortlist |
| 6 | Interview Scheduling | Proposes interview slots and drafts an invitation for the top candidate |
| 7 | End-to-End Flow | All steps above run as a single continuous pipeline |

## Design decisions

- **Two human-in-the-loop checkpoints.** The agent never auto-publishes a JD
  or auto-contacts candidates. It pauses for explicit recruiter approval
  after JD generation and after shortlisting — matching how the process was
  described by the stakeholder, and avoiding a fully "black box" hiring flow.
- **Claude is used for the two judgment-heavy steps only**: drafting the JD
  and scoring/ranking candidates against it. Both are prompted to return
  structured JSON so results can be rendered or processed programmatically,
  rather than parsed out of free text.
- **Platform posting and sourcing are simulated, not integrated.** Naukri.com,
  LinkedIn, and Indeed all require paid recruiter accounts, signed API
  agreements, and in some cases company verification before granting
  programmatic access. For this assignment, sourcing draws from a small local
  candidate pool so the full pipeline (JD → source → rank → schedule) can
  still be demonstrated end-to-end. `source_candidates()` is intentionally
  isolated so it can be swapped for real API calls later without touching
  the rest of the agent.
- **Interview scheduling drafts an invitation and proposes slots**, but does
  not sync with a real calendar (e.g. Google Calendar) or send real
  notifications — this is the other piece that would need a real backend
  integration for production use.

## Two ways to run it

### 1. Interactive browser demo (`agent-demo.html`)

A single self-contained HTML file — open it in any browser. It calls the
Claude API directly from the browser to generate the JD and rank candidates,
and walks through the pipeline step by step with a live status log. This is
the easiest way to **record a demo video**.

Run it locally with:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/agent-demo.html` in your browser (don't
just double-click the file — serving it locally avoids browser CORS issues).

Paste your own Anthropic API key into the **Anthropic API key** field at the
top of the page before clicking **Run agent**. The key is only held in
browser memory for that session — it is never written to disk, localStorage,
or sent anywhere except `api.anthropic.com`. Get a key from the
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
- **LLM reasoning** — Claude (`claude-sonnet-4-6`) drafts the JD and
  scores/ranks candidates, both returning structured JSON.
- **Sourcing** — `source_candidates()` reads from a local mock pool
  (`CANDIDATE_POOL`) standing in for real Naukri.com / LinkedIn / Indeed
  recruiter APIs.
- **Human-in-the-loop** — the agent stops and waits for explicit approval at
  two points rather than auto-publishing or auto-contacting candidates.

## Recording a demo

1. Open `agent-demo.html` in a browser (via `python3 -m http.server`, not by
   double-clicking).
2. Start screen recording (OBS, Loom, or your OS's built-in recorder).
3. Fill in a role (e.g. "Business Analyst" or "Mobile Developer"), openings,
   and skills, then click **Run agent**.
4. Narrate each step as it completes: requirement parsing → JD draft →
   approve → sourcing → AI shortlisting → approve → scheduling.
5. Mention that platform posting/sourcing and calendar sync are simulated
   for this assignment (see "Design decisions" above).
6. Export the recording and upload it (YouTube "unlisted" or Google Drive
   with link sharing works well for assignment submissions).

## Project structure

```
ai-recruitment-agent/
├── agent.py            # Python CLI implementation
├── agent-demo.html     # Interactive browser demo (for the video)
├── requirements.txt
├── .env.example
├── .gitignore
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
