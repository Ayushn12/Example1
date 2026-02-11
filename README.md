## Python Fitness Coach Chatbot (Strava-powered)

This repository now includes a Python chatbot that acts like a personal coach by:

- Pulling your recent activity data from Strava.
- Summarizing training load and sport focus.
- Building a weekly workout structure.
- Producing a diet guidance plan with calorie estimates.

## Project layout

- `fitness_chatbot/strava_client.py` – Strava API integration.
- `fitness_chatbot/planner.py` – Training summary + diet/workout plan generation.
- `fitness_chatbot/coach.py` – Chat-style interface that answers diet/workout/summary requests.
- `fitness_chatbot/main.py` – CLI entry point.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set your Strava access token:

```bash
export STRAVA_ACCESS_TOKEN="your_token_here"
```

## Run

```bash
python -m fitness_chatbot.main
```

Example prompts:

- `diet plan for this week`
- `what workout should i do today?`
- `show me my progress summary`

## Notes

- This starter focuses on practical heuristics and a clean structure.
- You can later add an LLM layer for richer natural language conversation while keeping the same planning pipeline.


## Push this project to your GitHub repository (same folder structure)

This project already uses a clean package layout (`fitness_chatbot/`, `tests/`, `requirements.txt`).
To publish it to your GitHub repo while preserving the same structure:

```bash
git remote add origin https://github.com/Ayushn12/fitness_python.git
# if origin already exists, update it instead:
# git remote set-url origin https://github.com/Ayushn12/fitness_python.git

git push -u origin HEAD
```

If GitHub asks for authentication, use a Personal Access Token (PAT) as your password for HTTPS pushes.
