# IFEval verdict audit

A reproducible audit of one IFEval instruction family: does the automatic verdict say what the instruction requires?

**Status:** framing (P1), started 2026-11-05. Nothing has been run yet.

## Object

- **Benchmark:** IFEval (Zhou et al., 2023, *Instruction-Following Evaluation for Large Language Models*), run through Inspect Evals.
- **Family audited:** `startend:end_checker` — "Finish your response with this exact phrase: …". The required phrase is stored as a parameter, `end_phrase`.

## Example

Illustrative item (not taken from the dataset), with `end_phrase = "Any other questions?"`:

> **Prompt:** Explain how volcanoes form. Finish your response with this exact phrase "Any other questions?". No other words should follow this phrase.

| Response ends with… | Expected verdict | Why |
|---|---|---|
| `…when magma rises. Any other questions?` | `True` | Ends with the exact phrase. |
| `…when magma rises. Any other questions? Have a nice day.` | `False` | Other words follow the phrase. |
| `…when magma rises. "Any other questions?"` | Ambiguous | The instruction does not say whether quotation marks around the phrase are allowed: `False` under a literal reading, `True` under an intent reading. |

The third row is the kind of case this audit is about: the verdict then depends on a convention chosen by the checker, not on the instruction.

## What the verdict measures

A `True` verdict asserts that the response ends with the requested phrase (`end_phrase`).

Two points are not settled by the instruction and are treated as **conventions** to be recorded, not as ground truth:

- what counts as "the same phrase" (letter case, quotation marks around the phrase);
- what counts as "the end" (trailing spaces, line breaks).

## What we will not conclude

A `True` verdict says nothing about:

- the relevance, factual accuracy or coherence of the response;
- the model's behaviour beyond this response (other samples, other prompts, other instruction families);
- safety.

## Intended use

Help someone comparing models on IFEval tell whether a score gap on this family reflects a real difference in following the instruction, or only a convention of the checker (case, quotes, end of text) — so that a model is not preferred or discarded because of a scoring artifact.

## Audit question

For this family and this version, where does the automatic verdict depend on a convention, and where does it diverge from the instruction? Which cases show it reproducibly?

## Method (planned)

1. Write expected verdicts from the instruction text, **before** reading the checker's code or output. Ambiguous cases record both readings instead of picking one.
2. Run the cases through the checker and compare, case by case: agreement, disagreement, or convention.
3. Check agreement between the instruction text, the stored `end_phrase` and the checker.
4. Compare findings with known issues (IFEval++, ACL 2026, appendix B.3) before claiming anything new.

## Constraints

- Pinned environment versions; item identifiers kept.
- No paid API calls at this stage: fixtures or a local model only (this tests the scoring pipeline, not a model).
- No proprietary or professional data in this repository.
