# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

An interactive idea evaluation tool. Users submit a business idea; the backend calls Claude to score it across four criteria (0–25 each, 100 total) and returns structured critique and guidance. Ideas scoring ≥ 70 are approved, otherwise rejected.

## Running the app

**Backend** (Python + FastAPI, port 8000):
```bash
cd backend
cp .env.example .env          # add your ANTHROPIC_API_KEY
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend** (React + Vite, port 5173):
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. The Vite dev server proxies `/api/*` to FastAPI.

## Architecture

**Data flow:**
1. `IdeaForm` POSTs `{ idea }` to `/api/evaluate`
2. `main.py` validates via Pydantic and delegates to `evaluator.py`
3. `evaluator.py` calls Claude (`claude-sonnet-4-6`) with a cached system prompt, parses the JSON response, computes `total_score`, and adds `approved`/`threshold` fields
4. `EvaluationResult` renders the response: verdict banner → four `ScoreCard`s → overall guidance → key risks

**Scoring model (in `evaluator.py` system prompt):**
- `value_proposition`, `business_benefits`, `feasibility`, `time_to_market` — each 0–25
- Threshold hardcoded at 70; change in both `evaluator.py` (default) and `EvaluationResult.jsx` if you want the UI label updated too

**Prompt caching:** The system prompt uses `cache_control: ephemeral` so repeated evaluations don't re-process the long rubric.

## Key files

| File | Role |
|------|------|
| `backend/evaluator.py` | Claude API call, JSON parsing, score aggregation |
| `backend/main.py` | FastAPI routes and CORS |
| `frontend/src/components/EvaluationResult.jsx` | Top-level result layout |
| `frontend/src/components/ScoreCard.jsx` | Per-criterion card with score bar |
| `frontend/vite.config.js` | API proxy config (`:5173 → :8000`) |
