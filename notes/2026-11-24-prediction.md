# Prediction before the first checker run (2026-11-24)

Written before running the checker and before reading its code.
Committed before the first run.

- **Checker:** `test_instruction_following` from the `josejg/instruction_following_eval` fork, `startend:end_checker`.
- **Strict:** the response as it is.
- **Loose:** the checker also tries modified versions of the response; one passing version is enough.

## Ambiguous cases

| id | expected_intent | predicted strict | predicted loose | why |
|---|---|---|---|---|
| lowercase_phrase | true | false | false | Loose transformations don't change the lowercase first letter. |
| quotes_around_phrase | true | false | false | Loose transformations only remove markdown stars, not quotes. |
| extra_punctuation_after | true | false | false | Loose transformations only remove markdown stars, not extra punctuation. |
| markdown_bold_one_word | true | false | true | Removing markdown formatting restores the exact phrase. |
| markdown_bold_whole_phrase | true | false | true | Removing markdown formatting restores the exact phrase. |
| trailing_newline | true | false | true | The trailing `\n` creates an empty last line; removing the last line fixes it. |

Hypothesis behind the strict column: strict compares raw characters (no lowercasing, no stripping of quotes or whitespace).

## Other cases (surprises only)

Clear and invalid cases where the checker might not give the expected verdict:

None expected: the checker should agree with `expected_intent` on all clear and invalid cases.

## Totals

- Disagreements with `expected_intent`, strict: 6 (the six ambiguous cases)
- Disagreements with `expected_intent`, loose: 3 (lowercase, quotes, extra punctuation)
- Disagreements with `expected_literal`, strict: 0

## Confidence

- Most confident about: `markdown_bold_one_word`, loose = true. The paper explicitly says loose removes `*` and `**`.
- Least confident about: `trailing_newline`, strict = false. If my hypothesis is wrong and strict trims whitespace before comparing, this case passes in strict too.
