# AI Travel Operations Agent

A multi-agent trip-planning system: LangGraph orchestrates specialized agents
(flight, hotel, activity, budget) with a conditional retry loop, backed by
FastAPI + PostgreSQL with real password authentication (JWT sessions), using
Groq for fast LLM reasoning, a full agentic AI trace with result links,
currency-aware budgeting (India -> INR, else USD), and a React + Tailwind
frontend.

## Setup

### 1. Database
```sql
CREATE DATABASE travel_agent_db;
```

### 2. Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```
Fill in `.env`:
- `DATABASE_URL` — your Postgres connection string
- `GROQ_API_KEY` — free at https://console.groq.com
- `JWT_SECRET_KEY` — generate one with:
  `python -c "import secrets; print(secrets.token_hex(32))"`

```bash
uvicorn main:app --reload --port 8000
```
If you ever see a "model_not_found" error from Groq, run `python llm_client.py`
from inside `backend/` to list every model your key currently has access to,
and update `MODEL_NAME` in that file.

### 3. Frontend
```bash
cd frontend
npm install
npm run dev
```
Opens at http://localhost:5500 by default (see `vite.config.js`).

### 4. Try it
- Sign up with country "India" → budget cap and every price shown in ₹
- Sign up with country "USA" (or anything else) → shown in $
- Enter a very low budget cap to see the "over budget, here's the closest
  plan" message and near-cap itinerary
- Log out and sign back in with the same email + password

### 5. API docs
http://localhost:8000/docs

## Authentication

Real password-based auth, not the email-only stand-in from earlier drafts:
- Passwords are hashed with PBKDF2-HMAC-SHA256 (260,000 iterations, random
  salt per user) — see `backend/auth.py`. Deliberately uses only Python's
  built-in `hashlib`, no extra dependency.
- `POST /auth/signup` and `POST /auth/login` both return a JWT access token
  (7-day expiry) plus the user's profile in one response.
- Every other endpoint requires that token in an `Authorization: Bearer
  <token>` header. `POST /plan/` identifies the user from the token, not
  from a `user_id` field in the request body — so nobody can plan a trip
  "as" a different user by editing the request.
- There's no password reset / email verification flow — out of scope for a
  portfolio project, but a natural next step.

## Project structure

```
backend/
  state.py            shared state object passed between agents
  graph.py             LangGraph orchestrator wiring
  auth.py               password hashing + JWT
  currency.py           India -> INR / else -> USD, conversions both ways
  trace.py               agentic trace logger + de-duplication for the UI
  agents/                one file per agent, plus combo_optimizer.py
  routes/                 auth.py, users.py, plan.py

frontend/
  src/api.js              fetch wrapper, attaches JWT to every request
  src/AuthContext.jsx      signed-in user + token, shared via React context
  src/pages/                Landing, Login, Signup, TripPlanner
  src/components/           Navbar, ItineraryTicket, TraceTimeline, etc.
```

## How the budget logic works

1. `flight_agent`, `hotel_agent`, `activity_agent` each just SEARCH (given
   an origin AND destination, not just a destination) and return their full
   list of options. Each option's trace entry includes the ACTUAL items
   found — name, cost in the user's currency, and its own route-specific
   link — not just a count and one generic link.
2. `budget_agent` first tries the full-value plan: cheapest flight +
   cheapest hotel + every activity.
3. If that's over budget, it loops back once and runs `combo_optimizer.py`
   — an exhaustive search over every flight × hotel × activity-subset
   combination — to find whichever spends the MOST without going OVER the
   cap. That's the "near budget cap" result.
4. If even the cheapest possible combination is still over budget, it stops
   (a second identical exhaustive search can't change the answer) and
   reports a best-effort plan with the exact shortfall shown.

All budget math happens in USD internally (the mock data is USD-priced).
Everything shown to the user — every line of the trace, not just the final
itinerary — is converted to their own currency.

**The trace shown in the UI only reflects the LATEST decision per agent**
(`trace.deduplicated_for_display`) — if budget_agent runs twice because of
the retry loop, only its final decision is shown; the earlier "over budget"
step doesn't linger in the UI. The full, un-deduplicated trace (every
attempt) is still saved to the database.

## Notes

- Flight/hotel data is mocked by default (see `TODO` comments in
  `backend/agents/flight_agent.py` / `hotel_agent.py`) — swap in a real API
  (e.g. Amadeus) when ready.
- To switch the LLM from Groq to Google Gemini, only `backend/llm_client.py`
  needs to change — see the comment block at the top of that file.
- The frontend's design system (colors, type, the boarding-pass itinerary
  card, the departures-board trace timeline) lives in
  `frontend/tailwind.config.js` and the component files — it's meant to
  visually echo what the app actually does (a multi-agent "ops board"),
  not generic template styling.
