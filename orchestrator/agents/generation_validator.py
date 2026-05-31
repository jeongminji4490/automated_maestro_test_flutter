# agents/generation_validator.py

class GenerationValidationError(ValueError):
    pass


class GenerationValidator:
    """
    Minimal text-based validation:
    1) appId header exists
    2) --- separator exists
    3) At least one of launchApp or openLink exists
    """

    def validate(self, yaml_text: str) -> str:
        if not isinstance(yaml_text, str) or not yaml_text.strip():
            raise GenerationValidationError("Generated YAML is empty.")

        lines = [line.strip() for line in yaml_text.splitlines() if line.strip()]

        # 1) appId header
        if not lines or not lines[0].startswith("appId:"):
            raise GenerationValidationError("Missing 'appId:' header on first line.")

        # Additional check to ensure appId value is not empty
        app_id_value = lines[0].replace("appId:", "", 1).strip()
        if not app_id_value:
            raise GenerationValidationError("appId value is empty.")

        # 2) --- separator
        if "---" not in lines:
            raise GenerationValidationError("Missing YAML separator '---'.")

        # 3) launchApp or openLink exists
        has_launch = any(line.startswith("- launchApp") for line in lines)
        open_link_lines = [line for line in lines if line.startswith("- openLink:")]
        has_open_link = len(open_link_lines) > 0

        if not (has_launch or has_open_link):
            raise GenerationValidationError(
                "YAML must contain either '- launchApp' or '- openLink:'."
            )

        # Additional check to ensure openLink value is not empty
        for open_link_line in open_link_lines:
            open_link_value = open_link_line.replace("- openLink:", "", 1).strip()
            open_link_value = open_link_value.strip('"').strip("'")
            if not open_link_value:
                raise GenerationValidationError("openLink value is empty.")

        return yaml_text