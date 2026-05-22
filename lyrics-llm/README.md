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
Three viable approach tracks are scoped — pick one before writing more code.

- Locked decisions: [`docs/00-scope.md`](./docs/00-scope.md).
- Field notes (state of AI lyric/poetry generation, May 2026): [`docs/01-field-notes.md`](./docs/01-field-notes.md).
- Frontier-LLM alternative path (Tracks A / B / Hybrid): [`docs/02-frontier-llm-alt-path.md`](./docs/02-frontier-llm-alt-path.md).
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
├── README.md                          this file
├── ROADMAP.md                         milestones and decisions
├── REFERENCES.md                      curated reading list
├── requirements.txt                   Phase 0 deps
├── configs/                           training / eval configs (later phases)
├── data/
│   └── seed_artists.json              sertanejo artist seed list (Phase 1)
├── scripts/
│   └── zero_shot.py                   Phase 0 zero-shot eval runner
├── notebooks/
│   └── 00_zero_shot_sertanejo.ipynb   Colab T4 notebook for Phase 0
├── evaluation/
│   ├── README.md
│   └── prompts/sertanejo_prompts.json 20 sertanejo prompts (5 × 4 sub-genres)
└── docs/
    ├── 00-scope.md                    locked v0 scope decisions
    ├── 01-field-notes.md              field survey (issues + author approaches)
    ├── 02-frontier-llm-alt-path.md    Track A / B / Hybrid approach options
    └── 00-zero-shot-samples.md        template — filled in after Colab run
```

Lyrics are copyrighted, so raw corpora are **not** committed. Acquisition
scripts and metadata-only artifacts (e.g., the artist seed list) live in
`data/`.

## Quick links

- v0 base model: [`TucanoBR/Tucano-630m`](https://huggingface.co/TucanoBR/Tucano-630m).
- v1 stretch base: [`TucanoBR/Tucano-1b1-Instruct`](https://huggingface.co/TucanoBR/Tucano-1b1-Instruct).
- Closest prior art: [`rsmonteiro/gpt2-small-portuguese-lyrics`](https://huggingface.co/rsmonteiro/gpt2-small-portuguese-lyrics) (used as a comparison baseline).
- Closest controllable-lyrics paper: [Pasini et al. 2024 — arXiv 2405.05176](https://arxiv.org/abs/2405.05176).

## How to run Phase 0

1. Open `notebooks/00_zero_shot_sertanejo.ipynb` in **Google Colab** with the **T4 runtime**.
2. Run all cells. The notebook clones this branch, installs deps, and runs
   `scripts/zero_shot.py` over the three candidate models against the 20
   prompts in `evaluation/prompts/sertanejo_prompts.json`.
3. Results land in `docs/00-zero-shot-<model>.json`. Commit them back to the
   branch (last cell of the notebook has a templated push command).
4. Fill in `docs/00-zero-shot-samples.md` with your verdict — that's the
   Phase 0 exit criterion.

## Working agreement

- All development on branch `claude/ptbr-lyrics-llm-setup-E04UU` until the
  roadmap converges.
- No raw lyrics committed. Cleaned/derived artifacts only, and only if the
  source license allows.
- No model weights committed. Adapters and GGUF builds stay local or in
  private HF repos.
