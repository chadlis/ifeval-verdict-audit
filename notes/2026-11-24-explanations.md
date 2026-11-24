# Explanations of the first checker run (2026-11-24)

Observed results: `results/2026-11-24-end_checker_observed.txt`.
Prediction committed before the run: `notes/2026-11-24-prediction.md`.
Code read after the run: `instruction_following_eval` @ `0c495b2`,
`instructions.py` (`EndChecker`) and `evaluation.py` (`test_instruction_following`).

## What strict actually does

`EndChecker.check_following`:

```python
value = value.strip().strip('"').lower()
self._end_phrase = self._end_phrase.strip().lower()
return value.endswith(self._end_phrase)
```

Three normalisations of the response, in this order:

1. `strip()`: removes whitespace and newlines at both ends.
2. `strip('"')`: removes straight double quotes at both ends only (not curly quotes, not single quotes, not inside the text).
3. `lower()`: ignores letter case.

The expected phrase gets `strip()` and `lower()`, not `strip('"')`.

My hypothesis "strict compares raw characters" is refuted: strict is already lenient on case, outer quotes and trailing whitespace.

## Cases explained

| id | observed strict / loose | explanation |
|---|---|---|
| lowercase_phrase | True / True | `lower()` on both sides. |
| quotes_around_phrase | True / True | `strip('"')` removes the outer straight quotes. |
| trailing_newline | True / True | `strip()` removes the trailing `\n` before comparing. |
| extra_punctuation_after | False / False | After normalisation the response ends with `questions?!!!!`; `endswith` needs the phrase to be the exact suffix, and nothing removes trailing punctuation. Loose variants only remove `*` or whole lines, so none helps. |
| markdown_bold_one_word | False / True | Strict: the raw text `Any other **questions**?` contains `**` inside the phrase. Loose: the variant `response.replace("*", "")` removes every `*`, which restores the phrase. |
| markdown_bold_whole_phrase | False / True | Strict: `**` follows the question mark, and `strip()` only removes whitespace and outer straight quotes. Loose: same `replace("*", "")` variant. |
| prompt_param_mismatch | False / False | The checker compares with the stored `end_phrase` (kwargs), never with the prompt text the model saw. A model that follows the prompt exactly fails if the two disagree. Dataset defect, not a checker defect. |

## Found while reading the code

- **Random phrase when `end_phrase` is missing.** `EndChecker.build_description` does `self._end_phrase = random.choice(_ENDING_OPTIONS)` when `end_phrase` is `None`. The same method serves instruction generation and checking. If an item reaches the checker without `end_phrase`, the response is compared to a randomly chosen phrase, with no error and no seed: a wrong, non-reproducible verdict. Whether this happens on real items is not established.

## To verify on real data (next session)

1. For every `startend:end_checker` item of `google/IFEval`, as loaded by Inspect Evals: does the phrase in the prompt text match the stored `end_phrase` (exactly, and after `strip().lower()`)?
2. Is `end_phrase` non-null for all of them?
3. Does Google's original IFEval code have the same `random.choice` fallback?
