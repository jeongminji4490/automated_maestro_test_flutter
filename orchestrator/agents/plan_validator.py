# agents/plan_validator.py
from typing import Any, Dict, List

class PlanValidationError(ValueError):
    pass


class PlanValidator:
    # Policy: empty string is allowed for input value (e.g., empty-input validation tests).
    ALLOW_EMPTY_INPUT_VALUE = True

    # Policy in deep_link mode:
    # - 'deeplink' action is required at least once.
    # - 'open' action is optional (allowed).
    ALLOW_OPEN_ACTION_WITH_DEEPLINK = True

    ALLOWED_ACTIONS = {
        "open",               # -> launchApp
        "deeplink",           # -> openLink
        "tap",
        "input",
        "assert_visible",
        "assert_not_visible",
    }

    def validate(self, plan: Dict[str, Any], deep_link: str | None = None) -> Dict[str, Any]:
        if not isinstance(plan, dict):
            raise PlanValidationError("Plan must be a dict.")

        self._validate_app_id(plan)
        self._validate_steps_shape(plan)          # validate 'steps' key exists and is a list
        self._validate_action_fields(plan)        # validate field for action action
        self._validate_entry_action(plan, deep_link)  # validate required entry action based on deep_link presence

        return plan

    def _validate_app_id(self, plan: Dict[str, Any]) -> None:
        app_id = plan.get("appId")
        if not isinstance(app_id, str) or not app_id.strip():
            raise PlanValidationError("Missing/invalid 'appId' (non-empty string required).")

    def _validate_steps_shape(self, plan: Dict[str, Any]) -> None:
        steps = plan.get("steps")
        if steps is None:
            raise PlanValidationError("Missing 'steps' key.")
        if not isinstance(steps, list):
            raise PlanValidationError("'steps' must be a list.")

    def _validate_action_fields(self, plan: Dict[str, Any]) -> None:
        steps: List[Dict[str, Any]] = plan.get("steps", [])

        for i, step in enumerate(steps):
            if not isinstance(step, dict):
                raise PlanValidationError(f"steps[{i}] must be a dict.")

            action = step.get("action")
            if action not in self.ALLOWED_ACTIONS:
                raise PlanValidationError(f"steps[{i}].action invalid: {action}")

            if action in {"tap", "assert_visible", "assert_not_visible"}:
                if not isinstance(step.get("target"), str) or not step["target"].strip():
                    raise PlanValidationError(f"steps[{i}] '{action}' requires non-empty 'target'.")

            if action == "input":
                if not isinstance(step.get("target"), str) or not step["target"].strip():
                    raise PlanValidationError(f"steps[{i}] 'input' requires non-empty 'target'.")
                value = step.get("value")
                if not isinstance(value, str):
                    raise PlanValidationError(f"steps[{i}] 'input' requires string 'value'.")
                if not self.ALLOW_EMPTY_INPUT_VALUE and not value.strip():
                    raise PlanValidationError(f"steps[{i}] 'input' requires non-empty 'value'.")

    def _validate_entry_action(self, plan: Dict[str, Any], deep_link: str | None) -> None:
        steps: List[Dict[str, Any]] = plan.get("steps", [])
        actions = [s.get("action") for s in steps]

        if deep_link and deep_link.strip():
            if "deeplink" not in actions:
                raise PlanValidationError(
                    "deep_link was provided, but plan does not include 'deeplink' action."
                )

            route = plan.get("route")
            if not isinstance(route, str) or not route.strip():
                raise PlanValidationError(
                    "deep_link mode requires non-empty 'route' in plan."
                )

            if not self.ALLOW_OPEN_ACTION_WITH_DEEPLINK and "open" in actions:
                raise PlanValidationError(
                    "deep_link mode does not allow 'open' action by policy."
                )