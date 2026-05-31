# cli.py

import argparse
import sys

from agents.planner_agent import PlannerAgent, PlannerError
from agents.generator_agent import GeneratorAgent
from agents.runner_agent import RunnerAgent
from agents.plan_validator import PlanValidator, PlanValidationError
from agents.generation_validator import GenerationValidator, GenerationValidationError


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intent", required=True)
    parser.add_argument("--app-id", required=True)
    parser.add_argument("--deep-link", required=False)
    parser.add_argument("--test-name", required=True)
    args = parser.parse_args()

    planner = PlannerAgent(args.app_id, args.deep_link)
    plan_validator = PlanValidator()
    generator = GeneratorAgent()
    generation_validator = GenerationValidator()
    runner = RunnerAgent()

    # 1) Create plan
    try:
        plan = planner.run(args.intent)
    except PlannerError as e:
        print(f"[PLANNER FAILED] {e}")
        return 1

    # 1.1) Validate plan (guardrail)
    try:
        validated_plan = plan_validator.validate(plan, args.deep_link)
    except PlanValidationError as e:
        print(f"[PLAN VALIDATION FAILED] {e}")
        return 1

    # 2) Generate and save YAML
    yaml_text = generator.run(validated_plan)

    # 2.1) Validate generated YAML (guardrail)
    try:
        validated_yaml = generation_validator.validate(yaml_text)
    except GenerationValidationError as e:
        print(f"[GENERATION VALIDATION FAILED] {e}")
        return 1

    test_yaml_path = generator.save_yaml(validated_yaml, f"{args.test_name}.yaml")

    # 3) Execute
    is_success = runner.run_test(test_yaml_path)
    if not is_success:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
