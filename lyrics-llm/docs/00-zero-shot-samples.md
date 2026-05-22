# Phase 0 — Zero-shot sertanejo samples

Status: **template, awaiting Colab run.** Fill in after running
[`notebooks/00_zero_shot_sertanejo.ipynb`](../notebooks/00_zero_shot_sertanejo.ipynb).

## Run metadata

- Date:
- Hardware:
- Notebook commit:
- Result JSONs:
  - `docs/00-zero-shot-Tucano-630m.json`
  - `docs/00-zero-shot-Tucano-1b1-Instruct.json`
  - `docs/00-zero-shot-gpt2-small-portuguese-lyrics.json`

## Qualitative scoring (1-5 Likert)

Pick 3 representative prompts per sub-genre. Score each model's completion on
the four dimensions below. Average per model.

| Sub-genre | Prompt id | Dimension | Tucano-630m | Tucano-1b1-Instruct | gpt2-pt-lyrics |
|---|---|---|---|---|---|
| raiz | raiz-01 | grammatical | | | |
| raiz | raiz-01 | sertanejo fit | | | |
| raiz | raiz-01 | coherence | | | |
| raiz | raiz-01 | tropes used | | | |
| ... | | | | | |

(Repeat as needed. Or just write impressions in prose below — this is
personal-scope eval.)

## Notes per model

### TucanoBR/Tucano-630m

- Memory used on T4:
- Time per prompt:
- Strongest output:
- Weakest output:
- Notable failure modes (off-topic, repetition, hallucinated English, wrong sub-genre, …):

### TucanoBR/Tucano-1b1-Instruct

- Memory used on T4:
- Time per prompt:
- Strongest output:
- Weakest output:
- Notable failure modes:

### rsmonteiro/gpt2-small-portuguese-lyrics

- Memory used on T4:
- Time per prompt:
- Strongest output:
- Weakest output:
- Notable failure modes:

## Verdict

Pick one:

- [ ] **Proceed with `TucanoBR/Tucano-630m` as v0** — quality good enough,
      fine-tuning headroom is there.
- [ ] **Skip 630m, start v0 from `TucanoBR/Tucano-1b1-Instruct`** — only if
      Colab T4 holds the QLoRA fine-tune and quality jump is worth it.
- [ ] **Step down to `TucanoBR/Tucano-160m`** — only if 630m is too
      slow/unwieldy on the free T4.
- [ ] **Use a different base entirely** — reasoning here.

Free-form notes:

## Prompt-style adjustments before Phase 1

- Should the prompts include explicit structure hints (`<verso>`, `<refrão>`)?
- Should we shorten prompts so the model has more "lyric room" inside the
  300-token budget?
- Are any prompts ambiguous enough to mislead the model? Drop or rewrite.

## Open follow-ups
