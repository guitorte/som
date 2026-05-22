# lyrics-llm

A trainable LLM that writes Brazilian-Portuguese (pt-BR) **sertanejo** song
lyrics. Personal-use, free-tier compute only. Independent from the static
music-player frontend that also lives in this repo.

The goal: fine-tune an open pt-native LLM so it can produce new, idiomatic
sertanejo lyrics that respect basic song structure (verso / refrão / ponte),
syllable counts typical of sertanejo (often redondilha maior, 7-12 syllables),
and the AABB-heavy rhyme schemes the genre uses.

## Status

**Phase 0 — Feasibility check.** Scope is locked; no training code yet.

- Locked decisions: [`docs/00-scope.md`](./docs/00-scope.md).
- Phased plan: [`ROADMAP.md`](./ROADMAP.md).
- Resource index: [`REFERENCES.md`](./REFERENCES.md).

**Locked v0 choices:**

| Decision | Value |
|---|---|
| Use-case | Personal only — no public demo, no weight publishing |
| Genre | Sertanejo (raiz, universitário, sofrência, feminejo) |
| Compute | Free tier only (Colab T4, Kaggle 2×T4) |
| Base model | `TucanoBR/Tucano-630m` (v0) → `Tucano-1b1-Instruct` (v1) |
| Tokenizer | Tucano's, + structural special tokens |
| Demo surface | Local CLI / Ollama only |

## Folder layout

```
lyrics-llm/
├── README.md          this file
├── ROADMAP.md         milestones and decisions
├── REFERENCES.md      curated reading list
├── configs/           training / eval configs (axolotl, unsloth, lm-eval)
├── data/              data acquisition, cleaning, tokenization (gitignored content)
├── scripts/           CLI scripts for scraping, training, inference
├── notebooks/         exploratory analysis
├── evaluation/        rhyme/syllable/BERTScore harnesses
└── docs/              design notes, ADRs, eval reports
```

`data/` is intentionally empty: lyrics are copyrighted, so raw corpora are
**not** committed. Acquisition scripts live in `scripts/` and are run locally.

## Quick links

- v0 base model: [`TucanoBR/Tucano-630m`](https://huggingface.co/TucanoBR/Tucano-630m).
- v1 stretch base: [`TucanoBR/Tucano-1b1-Instruct`](https://huggingface.co/TucanoBR/Tucano-1b1-Instruct).
- Closest prior art: [`rsmonteiro/gpt2-small-portuguese-lyrics`](https://huggingface.co/rsmonteiro/gpt2-small-portuguese-lyrics) (used as a comparison baseline).
- Closest controllable-lyrics paper: [Pasini et al. 2024 — arXiv 2405.05176](https://arxiv.org/abs/2405.05176).

## Working agreement

- All development on branch `claude/ptbr-lyrics-llm-setup-E04UU` until the
  roadmap converges.
- No raw lyrics committed. Cleaned/derived artifacts only, and only if the
  source license allows.
- No model weights committed. Adapters and GGUF builds stay local or in
  private HF repos.
