import json
from typing import Any

import requests


class PlannerError(RuntimeError):
    pass

class PlannerAgent:
    def __init__(self, app_id, deep_link=None):
        self.app_id = app_id
        self.deep_link = deep_link

    def run(self, intent):
        payload = {
            "intent": intent,
            "app_id": self.app_id
        }
        if self.deep_link and self.deep_link.strip():
            payload["deep_link"] = self.deep_link.strip()

        try:
            response = requests.post("http://localhost:8000/plan", json=payload, timeout=15)
            response.raise_for_status()
        except requests.RequestException as e:
            raise PlannerError(f"Failed to call planner service: {e}") from e

        try:
            data = response.json()
        except ValueError as e:
            raise PlannerError("Planner returned a non-JSON response.") from e

        if not isinstance(data, dict):
            raise PlannerError("Planner response must be a JSON object.")

        plan_data: Any = data.get("plan", data)

        if isinstance(plan_data, str):
            try:
                plan_data = json.loads(plan_data)
            except json.JSONDecodeError as e:
                raise PlannerError("Planner returned invalid JSON string in 'plan'.") from e

        if not isinstance(plan_data, dict):
            raise PlannerError("Planner output must be a dict-like object.")

        if self.deep_link and self.deep_link.strip():
            plan_data["route"] = self.deep_link.strip()

        return plan_data
