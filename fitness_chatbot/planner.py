from __future__ import annotations

from collections import Counter
from statistics import mean
from typing import Iterable

from .models import Activity, UserProfile


def summarize_training(activities: Iterable[Activity]) -> dict[str, float | str]:
    activity_list = list(activities)
    if not activity_list:
        return {
            "weekly_distance_km": 0.0,
            "weekly_duration_h": 0.0,
            "weekly_calories": 0.0,
            "primary_sport": "General Fitness",
        }

    total_distance_km = sum(a.distance_m for a in activity_list) / 1000
    total_duration_h = sum(a.moving_time_s for a in activity_list) / 3600
    total_calories = sum(a.calories for a in activity_list)
    primary_sport = Counter(a.sport_type for a in activity_list).most_common(1)[0][0]

    return {
        "weekly_distance_km": round(total_distance_km, 2),
        "weekly_duration_h": round(total_duration_h, 2),
        "weekly_calories": round(total_calories, 0),
        "primary_sport": primary_sport,
    }


def estimate_daily_calories(profile: UserProfile, activities: Iterable[Activity]) -> int:
    # Mifflin-St Jeor (neutral baseline) + activity adjustment
    bmr = 10 * profile.weight_kg + 6.25 * profile.height_cm - 5 * profile.age + 5
    activity_list = list(activities)
    calories_samples = [a.calories for a in activity_list if a.calories > 0]
    avg_workout_calories = mean(calories_samples) if calories_samples else 250

    if "lose" in profile.goal.lower():
        goal_adjustment = -300
    elif "gain" in profile.goal.lower() or "muscle" in profile.goal.lower():
        goal_adjustment = 250
    else:
        goal_adjustment = 0

    tdee = bmr + (avg_workout_calories * min(profile.weekly_training_days, 7) / 7)
    return max(int(tdee + goal_adjustment), 1400)


def build_week_plan(profile: UserProfile, activities: Iterable[Activity]) -> dict[str, list[str] | str | int]:
    summary = summarize_training(activities)
    calories = estimate_daily_calories(profile, activities)
    sport = summary["primary_sport"]

    workouts = [
        f"{sport} endurance day: 45-60 minutes at easy-to-moderate pace",
        "Strength day: 40 minutes (squat, hinge, push, pull, core)",
        "Intervals day: 8 x 2-minute hard efforts with 2-minute recovery",
        "Mobility + recovery day: 20-30 minutes stretching and breath work",
    ]

    diet = [
        f"Target calories: ~{calories} kcal/day",
        "Protein: 1.6-2.2 g per kg body weight",
        "Carbs: prioritize whole grains, fruit, and vegetables around workouts",
        "Fats: include nuts, olive oil, seeds, and fatty fish",
        f"Preference adaptation: {profile.dietary_preference}",
        "Hydration: 30-35 ml water per kg body weight, plus extra after workouts",
    ]

    return {
        "coach_note": (
            f"Your current training volume is {summary['weekly_distance_km']} km and "
            f"{summary['weekly_duration_h']} hours/week. We'll progress gradually with "
            "one hard day, one long day, two strength/recovery focused days."
        ),
        "workouts": workouts[: max(3, min(4, profile.weekly_training_days))],
        "diet": diet,
        "daily_calorie_target": calories,
    }
