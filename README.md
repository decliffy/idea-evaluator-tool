# Idea Evaluator

An interactive business-idea evaluation tool. A user submits an idea; the backend
calls Claude to score it across four criteria (0–25 each, 100 total) and returns a
structured critique with actionable guidance. Ideas scoring **≥ 70** are approved.

## Features

- Single-page React UI for submitting an idea and viewing results
- Claude-powered scoring with candid critique and improvement suggestions per criterion
- Verdict banner (approved / rejected), per-criterion score cards, overall guidance, and key risks
- Serverless AWS deployment behind a global CDN (HTTPS, private origins)

## Scoring model

Each criterion is scored 0–25 by Claude; the backend sums them and applies the threshold (70):

| Criterion | What it measures |
|-----------|------------------|
| `value_proposition` | Clarity of the problem, target customer, differentiation |
| `business_benefits` | Revenue potential, market size, monetization, moat |
| `feasibility` | Technical/operational practicality, resources, regulation |
| `time_to_market` | How fast an MVP can reach first customers |

## Tech stack

- **Frontend:** React 18, Vite, Tailwind CSS
- **Backend:** Python 3.13, FastAPI, Pydantic, Anthropic SDK (`claude-sonnet-4-6`), Mangum (ASGI→Lambda adapter)
- **Infrastructure:** Terraform, AWS Lambda + Function URL, CloudFront (OAC), S3, CloudWatch
- **Tooling:** Docker (builds Linux-native Lambda dependencies), AWS CLI, Git/GitHub

## Architecture

```
Browser ──HTTPS──► CloudFront ──┬── default ──► S3 (private, OAC)        static React build
                                └── /api/*  ──► Lambda Function URL (OAC) FastAPI + Mangum
                                                     └──► Claude API (claude-sonnet-4-6)
```

CloudFront fronts both origins as one HTTPS domain (no CORS). The static build is
served from a private S3 bucket; `/api/*` is routed to a private Lambda Function URL.
Both origins are locked down with **Origin Access Control (OAC)** so they are only
reachable through CloudFront. See [`infra/architecture.png`](infra/architecture.png)
for the full diagram.

## Project structure

```
backend/    FastAPI app — main.py (routes), evaluator.py (Claude call + scoring)
frontend/   React + Vite SPA — src/App.jsx makes the single /api/evaluate call
infra/      Terraform config, build/deploy scripts, and deployment docs
```

## Local development

**Backend** (FastAPI, port 8000):

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

Open http://localhost:5173 — the Vite dev server proxies `/api/*` to FastAPI.

## Deployment

The app is deployed to AWS with Terraform. See [`infra/README.md`](infra/README.md)
for the full deploy steps and the OAC / Mangum / ASGI background:

```bash
./infra/build_lambda.sh                       # build Lambda package (Docker)
cd infra && terraform apply                    # provision infrastructure
./deploy_frontend.sh                           # build + publish frontend, invalidate CDN
```
