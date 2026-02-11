from __future__ import annotations

import os
from datetime import datetime
from typing import List

import requests

from .models import Activity


class StravaClient:
    """Small Strava API wrapper for reading recent activities."""

    BASE_URL = "https://www.strava.com/api/v3"

    def __init__(self, access_token: str | None = None) -> None:
        self.access_token = access_token or os.getenv("STRAVA_ACCESS_TOKEN")
        if not self.access_token:
            raise ValueError(
                "Missing Strava access token. Set STRAVA_ACCESS_TOKEN in your environment."
            )

    def fetch_recent_activities(self, per_page: int = 15) -> List[Activity]:
        response = requests.get(
            f"{self.BASE_URL}/athlete/activities",
            headers={"Authorization": f"Bearer {self.access_token}"},
            params={"per_page": per_page},
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()

        activities: list[Activity] = []
        for item in payload:
            activities.append(
                Activity(
                    name=item.get("name", "Activity"),
                    sport_type=item.get("sport_type", "Workout"),
                    distance_m=float(item.get("distance", 0.0)),
                    moving_time_s=int(item.get("moving_time", 0)),
                    total_elevation_gain_m=float(item.get("total_elevation_gain", 0.0)),
                    calories=float(item.get("calories") or 0.0),
                    start_date_local=datetime.fromisoformat(
                        item.get("start_date_local", "1970-01-01T00:00:00Z").replace("Z", "+00:00")
                    ),
                )
            )
        return activities
