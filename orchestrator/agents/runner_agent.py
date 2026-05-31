# agents/runner_agent.py

import subprocess

class RunnerAgent:
    def __init__(
        self,
        maestro_cmd="maestro"
    ):
        self.maestro_cmd = maestro_cmd

    def run_test(self, yaml_path: str) -> bool:
        # Contract: return True on success, False on failure; caller maps to process exit code.
        print(f"Running test: {yaml_path}")

        result = subprocess.run(
            [self.maestro_cmd, "test", yaml_path],
            capture_output=True,
            text=True
        )

        print("=== OUTPUT ===")
        print(result.stdout)

        if result.returncode != 0:
            print("TEST FAILED")
            print(result.stderr)
        else:
            print("TEST PASSED")

        return result.returncode == 0
