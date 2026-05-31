# agents/generator_agent.py

import os

class GeneratorAgent:
    def __init__(self, project_root="/Users/jeongminji/Play/automated_flutter_ui_test/maestro_test"):
        self.project_root = project_root

    def save_yaml(self, yaml_text: str, filename: str):
        maestro_dir = os.path.join(self.project_root, "maestro")
        os.makedirs(maestro_dir, exist_ok=True)

        path = os.path.join(maestro_dir, filename)
        with open(path, "w") as f:
            f.write(yaml_text)

        return path

    def run(self, plan: dict):
        app_id = plan["appId"]
        steps = plan["steps"]

        yaml_blocks = []

        yaml_blocks.append(f"appId: {app_id}")
        yaml_blocks.append("---")

        for step in steps:
            action = step["action"]

            if action == "open":
                yaml_blocks.append("- launchApp")

            elif action == "deeplink":
                yaml_blocks.append(f'- openLink: "{plan.get("route", "")}"')

            elif action == "tap":
                yaml_blocks.append(f'- tapOn: "{step["target"]}"')

            elif action == "input":
                yaml_blocks.append(
                    f'- tapOn: "{step["target"]}"\n'
                    f'- inputText: "{step["value"]}"'
                )

            elif action == "assert_visible":
                yaml_blocks.append(f'- assertVisible: "{step["target"]}"')

            elif action == "assert_not_visible":
                yaml_blocks.append(f'- assertNotVisible: "{step["target"]}"')

        return "\n\n".join(yaml_blocks)
