from __future__ import annotations

import json
from dataclasses import asdict

from .models import UserProfile
from .planner import build_week_plan, summarize_training
from .strava_client import StravaClient


class FitnessCoachBot:
    """Chat-style orchestration layer combining Strava + planning logic."""

    def __init__(self, profile: UserProfile, strava_client: StravaClient) -> None:
        self.profile = profile
        self.strava_client = strava_client

    def generate_report(self) -> dict:
        activities = self.strava_client.fetch_recent_activities(per_page=20)
        summary = summarize_training(activities)
        plan = build_week_plan(self.profile, activities)

        return {
            "profile": asdict(self.profile),
            "training_summary": summary,
            "plan": plan,
        }

    def chat(self, user_message: str) -> str:
        report = self.generate_report()
        normalized = user_message.lower()

        if "diet" in normalized or "meal" in normalized:
            return "\n".join(report["plan"]["diet"])

        if "workout" in normalized or "exercise" in normalized:
            return "\n".join(report["plan"]["workouts"])

        if "summary" in normalized or "progress" in normalized:
            return json.dumps(report["training_summary"], indent=2)

        return (
            "I can help with your weekly plan. Ask for 'diet', 'workout', or 'summary'.\n\n"
            f"Coach note: {report['plan']['coach_note']}"
        )
