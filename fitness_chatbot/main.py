from __future__ import annotations

from .coach import FitnessCoachBot
from .models import UserProfile
from .strava_client import StravaClient


def build_default_profile() -> UserProfile:
    return UserProfile(
        age=30,
        weight_kg=72,
        height_cm=175,
        goal="Lose fat while improving endurance",
        dietary_preference="High-protein Mediterranean",
        weekly_training_days=4,
    )


def run_cli() -> None:
    profile = build_default_profile()
    bot = FitnessCoachBot(profile, StravaClient())

    print("Fitness Coach Bot is ready. Type 'exit' to quit.")
    while True:
        message = input("You: ").strip()
        if message.lower() in {"exit", "quit"}:
            print("Coach: See you at the next session!")
            break
        reply = bot.chat(message)
        print(f"Coach: {reply}\n")


if __name__ == "__main__":
    run_cli()
