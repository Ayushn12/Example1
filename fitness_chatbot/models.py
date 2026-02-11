from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Activity:
    """Simplified Strava activity model used by the coach logic."""

    name: str
    sport_type: str
    distance_m: float
    moving_time_s: int
    total_elevation_gain_m: float
    calories: float
    start_date_local: datetime


@dataclass
class UserProfile:
    """Static information used to personalize plans."""

    age: int
    weight_kg: float
    height_cm: float
    goal: str
    dietary_preference: str
    weekly_training_days: int
