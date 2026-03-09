from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import random
from typing import Dict, List, Optional

import feedparser
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pydantic import BaseModel, Field


TOPICS = [
    "AI",
    "AI Agents",
    "Automation",
    "Startups",
    "Open Source Tools",
    "Productivity",
    "Future of Work",
    "Cybersecurity",
    "Developer Tools",
    "No-Code / Low-Code",
    "Tech Innovations",
    "n8n",
]

RSS_FEEDS = {
    "AI": [
        "https://openai.com/blog/rss.xml",
        "https://venturebeat.com/category/ai/feed/",
    ],
    "AI Agents": [
        "https://venturebeat.com/category/ai/feed/",
        "https://techcrunch.com/category/artificial-intelligence/feed/",
    ],
    "Automation": [
        "https://techcrunch.com/tag/automation/feed/",
        "https://www.theverge.com/rss/index.xml",
    ],
    "n8n": [
        "https://blog.n8n.io/rss/",
        "https://techcrunch.com/tag/automation/feed/",
    ],
}

DEFAULT_FEEDS = [
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
]


class GenerateRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=80)
    audience: str = Field(default="LinkedIn professionals", min_length=3, max_length=120)
    tone: str = Field(default="Founder-level, conversational, authoritative", max_length=120)


@dataclass
class TrendItem:
    title: str
    source: str
    published: str


class TrendResearcher:
    def fetch_trends(self, topic: str, limit: int = 5) -> List[TrendItem]:
        feeds = RSS_FEEDS.get(topic, []) + DEFAULT_FEEDS
        items: List[TrendItem] = []

        for url in feeds:
            parsed = feedparser.parse(url)
            source_title = parsed.feed.get("title", "Unknown source") if parsed.feed else "Unknown source"
            for entry in parsed.entries[:4]:
                title = entry.get("title")
                if not title:
                    continue
                published = entry.get("published", "recently")
                items.append(TrendItem(title=title.strip(), source=source_title, published=published))

        deduped: Dict[str, TrendItem] = {}
        for item in items:
            deduped[item.title.lower()] = item

        results = list(deduped.values())[:limit]
        if not results:
            raise HTTPException(status_code=503, detail="Unable to fetch live trend data right now.")

        return results


class ViralPostStrategist:
    hooks = [
        "Most teams are underestimating this shift in {topic} — and it's going to cost them.",
        "If you're still treating {topic} like a side project, you're already behind.",
        "I keep seeing smart teams make the same {topic} mistake in 2026.",
        "The gap between leaders and laggards in {topic} just got wider this week.",
    ]

    closing_questions = [
        "Are you building for today's workflows — or tomorrow's edge?",
        "What are you changing in your stack this quarter?",
        "Is your team experimenting fast enough to stay relevant?",
        "Would your current strategy survive a 10x speedup in this space?",
    ]

    def create_post(self, topic: str, audience: str, tone: str, trends: List[TrendItem]) -> str:
        now = datetime.now(timezone.utc).strftime("%d %b %Y")
        hook = random.choice(self.hooks).format(topic=topic)
        close = random.choice(self.closing_questions)

        trend_lines = [f"• {item.title} ({item.source})" for item in trends[:3]]

        hashtags = self._hashtags(topic)

        lines = [
            hook,
            "",
            f"Real-time signal check ({now}): {trends[0].title}.",
            f"This is bigger than hype — it's reshaping how {audience.lower()} create value.",
            "",
            "Here’s the mini-lesson:",
            "Speed wins only when paired with distribution + trust.",
            "",
            "What smart operators are doing now:",
            *trend_lines,
            "• Converting trend noise into one clear weekly execution bet",
            "",
            "If your team waits for certainty, you'll miss the compounding window.",
            close,
            "",
            hashtags,
        ]

        # Keep within 9-25 lines
        return "\n".join(lines[:25])

    def _hashtags(self, topic: str) -> str:
        topic_tag = topic.lower().replace(" ", "").replace("/", "")
        common = ["#ArtificialIntelligence", "#Automation", "#FutureOfWork", "#TechTrends", "#Innovation"]
        if topic.lower() == "n8n":
            common = ["#n8n", "#Automation", "#NoCode", "#AI", "#Productivity"]
        elif "security" in topic.lower():
            common = ["#Cybersecurity", "#DevSecOps", "#TechLeadership", "#RiskManagement", "#Innovation"]

        if not any(tag.lower() == f"#{topic_tag}" for tag in common):
            common[0] = f"#{topic_tag.capitalize()}"

        return " ".join(common[:5])


class VisualPromptDirector:
    def generate_prompt_json(self, topic: str, trends: List[TrendItem]) -> Dict[str, str]:
        return {
            "topic": topic,
            "style": "modern, minimal, professional LinkedIn style",
            "scene": f"Editorial-style composition representing {topic} momentum with subtle UI dashboards and human collaboration",
            "focus": trends[0].title,
            "color_palette": "clean white, deep blue, neutral gray with a single electric accent",
            "aspect_ratio": "1:1",
            "text_overlay": "Short bold statement, max 6 words",
        }


class ExpertOrchestrator:
    """CrewAI/LangChain-inspired orchestrator with deterministic fallback."""

    def __init__(self) -> None:
        self.researcher = TrendResearcher()
        self.strategist = ViralPostStrategist()
        self.visual = VisualPromptDirector()

    def run(self, req: GenerateRequest) -> Dict[str, object]:
        trends = self.researcher.fetch_trends(req.topic)
        post = self.strategist.create_post(req.topic, req.audience, req.tone, trends)
        image_prompt = self.visual.generate_prompt_json(req.topic, trends)
        return {
            "topic": req.topic,
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "trends": [t.__dict__ for t in trends],
            "post": post,
            "image_prompt": image_prompt,
        }


app = FastAPI(title="LinkedIn Viral Tech Post Studio")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
orchestrator = ExpertOrchestrator()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "topics": TOPICS})


@app.get("/api/trends")
def trends(topic: Optional[str] = None):
    selected = topic or "AI"
    return {
        "topic": selected,
        "items": [t.__dict__ for t in orchestrator.researcher.fetch_trends(selected)],
    }


@app.post("/api/generate-post")
def generate_post(req: GenerateRequest):
    if req.topic not in TOPICS:
        raise HTTPException(status_code=400, detail="Unsupported topic.")
    return orchestrator.run(req)
