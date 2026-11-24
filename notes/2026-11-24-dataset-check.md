# Real-data check of `end_phrase` (2026-11-24)

Question: for the `startend:end_checker` items of `google/IFEval`, is the stored `end_phrase` always present, and does it match the phrase written in the prompt text?

## Prediction (written before loading the data)

- Number of `end_checker` items: about 20 out of 541.
- Disagreements between prompt text and stored `end_phrase`: few, if the instruction text was generated from the parameter.
- Null `end_phrase`: 

## Result

Script: [`scripts/check_end_phrase_dataset.py`](../scripts/check_end_phrase_dataset.py), on `google/IFEval` as downloaded from Hugging Face.

```
startend:end_checker items: 26 / 541
null end_phrase:            0
not in prompt (exact):      0
not in prompt (normalised): 0
```

- Count: 26 items, close to the predicted ~20.
- No null `end_phrase`, and every stored phrase appears verbatim in its prompt. Consistent with the prediction.

## What this establishes, and what it does not

- On the raw Hugging Face data, the two defects shown on synthetic cases do not occur for this family: no item would reach the checker without `end_phrase`, and no prompt names a phrase absent from its parameter.
- The check is weak on one side: "the stored phrase appears somewhere in the prompt" does not prove it is the phrase the instruction asks for (it could appear elsewhere). With 0 failures this does not change the result, but a stricter check would parse the instruction sentence.
- This is the raw dataset, not the data as loaded by Inspect Evals. If that pipeline transforms `kwargs` (for example drops `None` keys or renames fields), the `random.choice` fallback could still be reached. To check in the Inspect session.
