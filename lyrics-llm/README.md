# lyrics-llm

A trainable LLM that writes Brazilian-Portuguese (pt-BR) song lyrics.

This sub-project is the ML side of the `som` repo (which already hosts a static
pt-BR music player). The goal is to fine-tune an open LLM so it can produce
new, idiomatic pt-BR lyrics that respect basic song structure (verse / chorus /
bridge), syllable counts, and rhyme — and optionally condition on genre,
mood, or a seed line.

## Status

**Phase 0 — Planning.** No code or model yet. See:

- [`ROADMAP.md`](./ROADMAP.md) — phased plan from data collection to deployment.
- [`REFERENCES.md`](./REFERENCES.md) — curated index of base models, datasets,
  papers, tooling, communities, and known legal/ethical risks.

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

- Brazilian Portuguese base LLMs: TucanoBR, Sabiá, Bode, GlórIA — see
  [`REFERENCES.md#1-brazilian-portuguese-base--foundation-llms`](./REFERENCES.md#1-brazilian-portuguese-base--foundation-llms).
- Closest prior art: `rsmonteiro/gpt2-small-portuguese-lyrics` (GPT-2 small, MIT).
- Closest controllable-lyrics paper: Pasini et al. 2024 (arXiv 2405.05176).

## Working agreement

- All development on branch `claude/ptbr-lyrics-llm-setup-E04UU` until the
  roadmap converges.
- No raw lyrics committed. Cleaned/derived artifacts only, and only if the
  source license allows.
