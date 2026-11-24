"""Run the 15 end_checker cases through the official IFEval checker.

Calls `test_instruction_following` directly (no model, no Inspect),
once in strict mode and once in loose mode, and prints one row per case.

Usage: uv run python scripts/run_end_checker.py
"""

from pathlib import Path

import yaml
from instruction_following_eval.evaluation import test_instruction_following

CASES_FILE = Path(__file__).parent.parent / "cases" / "end_checker_expected.yaml"
INSTRUCTION_ID = "startend:end_checker"


def build_example(data: dict, case: dict, key: int) -> dict:
    """Build the IFEval item the checker sees for one case."""
    prompt = case.get("prompt_override", data["prompt"])
    end_phrase = case.get("end_phrase_override", data["end_phrase"])
    return {
        "key": key,
        "instruction_id_list": [INSTRUCTION_ID],
        "prompt": prompt,
        "kwargs": [{"end_phrase": end_phrase}],
    }


def verdict(example: dict, response: str, strict: bool) -> bool:
    return test_instruction_following(example, response, strict=strict).follow_all_instructions


def main() -> None:
    data = yaml.safe_load(CASES_FILE.read_text())

    header = f"{'id':<28} {'literal':<8} {'intent':<8} {'strict':<8} {'loose':<8}"
    print(header)
    print("-" * len(header))

    for key, case in enumerate(data["cases"]):
        example = build_example(data, case, key)
        response = case["response"]
        strict = verdict(example, response, strict=True)
        loose = verdict(example, response, strict=False)
        print(
            f"{case['id']:<28} {str(case['expected_literal']):<8} "
            f"{str(case['expected_intent']):<8} {str(strict):<8} {str(loose):<8}"
        )


if __name__ == "__main__":
    main()
