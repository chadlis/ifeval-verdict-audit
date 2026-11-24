# Real-data check of `end_phrase` (2026-11-24)

Question: for the `startend:end_checker` items of `google/IFEval`, is the stored `end_phrase` always present, and does it match the phrase written in the prompt text?

## Prediction (written before loading the data)

- Number of `end_checker` items: about 20 out of 541.
- Disagreements between prompt text and stored `end_phrase`: few, if the instruction text was generated from the parameter.
- Null `end_phrase`: 

## Result

