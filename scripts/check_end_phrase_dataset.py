"""Check `end_phrase` against the prompt text on the real IFEval items.

For every item of google/IFEval that contains `startend:end_checker`:
- is the stored `end_phrase` null?
- does it appear in the prompt exactly?
- does it appear after the checker's normalisation (strip + lower)?

Usage: uv run python scripts/check_end_phrase_dataset.py
"""

from datasets import load_dataset

INSTRUCTION_ID = "startend:end_checker"


def main() -> None:
    ds = load_dataset("google/IFEval", split="train")

    rows = []
    for item in ds:
        if INSTRUCTION_ID not in item["instruction_id_list"]:
            continue
        idx = item["instruction_id_list"].index(INSTRUCTION_ID)
        kw = item["kwargs"][idx]
        end_phrase = kw.get("end_phrase")

        is_null = end_phrase is None
        in_prompt_exact = not is_null and end_phrase in item["prompt"]
        in_prompt_normalised = (
            not is_null and end_phrase.strip().lower() in item["prompt"].lower()
        )

        rows.append((item["key"], end_phrase, is_null, in_prompt_exact,
                     in_prompt_normalised, item["prompt"][-120:]))

    print(f"{INSTRUCTION_ID} items: {len(rows)} / {len(ds)}")
    print(f"null end_phrase:            {sum(r[2] for r in rows)}")
    print(f"not in prompt (exact):      {sum(not r[3] for r in rows)}")
    print(f"not in prompt (normalised): {sum(not r[4] for r in rows)}")

    print("\nItems failing at least one check:")
    for key, phrase, is_null, exact, norm, tail in rows:
        if is_null or not exact or not norm:
            print(f"- key={key} end_phrase={phrase!r} exact={exact} normalised={norm}")
            print(f"  prompt ends: ...{tail!r}")


if __name__ == "__main__":
    main()
