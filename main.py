# main.py
from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

SLACK_TOKEN = os.environ.get("SLACK_TOKEN")

SLACK_API_URL = "https://slack.com/api/users.profile.set"

STATUS_MAP = {
    "Work": {"text": "Deep Work 🧠", "emoji": ":brain:"},
    "Personal": {"text": "Personal Time 🌴", "emoji": ":palm_tree:"},
    "Sleep": {"text": "Sleeping 😴", "emoji": ":zzz:"},
    "Communting": {"text": "Communting 🚙", "emoji": ":blue_car:"},
    "Off": {"text": "", "emoji": ""}  # clears status
}

async def set_slack_status(text: str, emoji: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            SLACK_API_URL,
            headers={
                "Authorization": f"Bearer {SLACK_TOKEN}",
                "Content-Type": "application/json"
            },
            json={"profile": {"status_text": text, "status_emoji": emoji}}
        )
        print("Slack response:", response.status_code, response.text)
        return response.json()

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/focus-mode")
async def focus_mode(request: Request):
    data = await request.json()
    mode = data.get("mode", "Off")
    status = STATUS_MAP.get(mode, STATUS_MAP["Off"])
    await set_slack_status(status["text"], status["emoji"])
    return {"message": f"Slack status updated for mode: {mode}"}
