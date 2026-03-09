# LinkedIn Viral Tech Post Studio

A lightweight full-stack web tool that creates high-engagement LinkedIn post drafts about trending technology topics.

## What it does

- Pulls recent technology trend headlines from live RSS feeds.
- Uses an **Expert Orchestrator** pipeline inspired by **LangChain + CrewAI** roles:
  - Trend Researcher
  - Viral Copy Strategist
  - LinkedIn Editor
  - Visual Prompt Director
- Generates LinkedIn-ready posts with:
  - scroll-stopping hook
  - concise insight + takeaway
  - mini breakdown bullets
  - thought-provoking close
  - 4–6 relevant hashtags
- Generates JSON image prompts (modern, minimal, professional LinkedIn style).

## Stack

- Backend: FastAPI (Python)
- Frontend: Vanilla HTML/CSS/JS
- Live trend sources: RSS feeds (TechCrunch, VentureBeat AI, The Verge Tech, OpenAI blog)

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

Open: `http://localhost:8000`

## API

- `GET /api/trends` – latest trend headlines by topic
- `POST /api/generate-post` – generates LinkedIn post + image prompt JSON

## Notes

- If optional LangChain / CrewAI packages are installed and configured with your preferred LLM credentials, you can extend the `ExpertOrchestrator` class for true model-powered generation.
- Fallback generator is deterministic and does not require API keys, so the app works immediately.
