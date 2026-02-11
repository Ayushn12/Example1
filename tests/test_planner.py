from datetime import datetime

from fitness_chatbot.models import Activity, UserProfile
from fitness_chatbot.planner import build_week_plan, summarize_training


def sample_activities() -> list[Activity]:
    now = datetime.now()
    return [
        Activity("Easy Run", "Run", 5000, 1800, 40, 420, now),
        Activity("Long Ride", "Ride", 22000, 3600, 120, 700, now),
        Activity("Tempo Run", "Run", 7000, 2200, 60, 500, now),
    ]


def test_summarize_training_computes_totals() -> None:
    summary = summarize_training(sample_activities())
    assert summary["weekly_distance_km"] == 34.0
    assert summary["primary_sport"] == "Run"


def test_build_week_plan_contains_core_sections() -> None:
    profile = UserProfile(29, 70, 174, "Lose fat", "Vegetarian", 4)
    plan = build_week_plan(profile, sample_activities())
    assert "coach_note" in plan
    assert len(plan["workouts"]) >= 3
    assert plan["daily_calorie_target"] >= 1400
