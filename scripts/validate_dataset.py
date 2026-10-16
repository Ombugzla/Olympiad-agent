import json
from pathlib import Path

DATASET_PATH = Path("problems/problems.json")

REQUIRED_FIELDS = {"id", "problem", "solution", "answer"}


def validate_dataset():
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        problems = json.load(file)

    if not isinstance(problems, list):
        raise ValueError("Dataset must be a JSON list.")

    seen_ids = set()
    errors = []

    for index, problem in enumerate(problems):
        if not isinstance(problem, dict):
            errors.append(f"Record {index}: expected an object.")
            continue

        missing = REQUIRED_FIELDS - problem.keys()

        if missing:
            errors.append(
                f"Record {index}: missing fields {sorted(missing)}"
            )
            continue

        problem_id = problem["id"]

        if not isinstance(problem_id, str) or not problem_id.strip():
            errors.append(f"Record {index}: invalid ID.")
        elif problem_id in seen_ids:
            errors.append(f"Record {index}: duplicate ID {problem_id}.")
        else:
            seen_ids.add(problem_id)

        for field in ("problem", "solution", "answer"):
            if not isinstance(problem[field], str) or not problem[field].strip():
                errors.append(
                    f"Record {index} ({problem_id}): "
                    f"{field} must be a non-empty string."
                )

    if errors:
        print("Dataset validation FAILED:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("Dataset validation PASSED!")
    print(f"Total problems: {len(problems)}")
    print(f"Unique IDs: {len(seen_ids)}")


if __name__ == "__main__":
    validate_dataset()
