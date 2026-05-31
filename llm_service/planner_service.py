from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI
from pathlib import Path
import os

load_dotenv()

PROMPT_TEMPLATE = Path("prompts/planner.md").read_text()

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/plan")
def plan(req: dict):
    intent = req["intent"]

    prompt = (
      PROMPT_TEMPLATE
        .replace("<USER_INTENT>", intent)
        .replace("<APP_ID>", req.get("app_id", ""))
        .replace("<DEEP_LINK>", req.get("deep_link", ""))
    )

    response = client.responses.create(
        model="gpt-4.1",
        input=prompt
    )

    return {"plan": response.output_text}