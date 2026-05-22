# Scope decisions — v0 (locked 2026-05-22)

These are the four upstream choices the rest of the roadmap depends on, plus
the immediate implications. Revisit if the situation changes.

## 1. Use-case — **personal only**

- No public demo, no shared endpoint, no model-weight publishing.
- No commercial use.
- Implication: copyright pressure is significantly lower in practice
  (no redistribution, no monetization), but we still keep raw lyric corpora
  out of git so the repo itself does not republish anything.

## 2. Genre — **sertanejo**

- Single-genre focus. Universo, sertanejo raiz, sertanejo universitário,
  sofrência, and feminejo all count.
- Implication: a much smaller corpus is workable (~5k-15k songs target),
  data acquisition can be more curated, and evaluation can use
  sertanejo-specific tropes (hyperbolic heartbreak, agropecuária imagery,
  rural-urban contrast, end-rhyme heavy AABB schemes) as quality signals.

## 3. Compute — **free tier only**

- Google Colab free (T4 16GB) and Kaggle (2× T4 16GB, ~30h/week) only.
- No paid GPU rental.
- Implication: base-model selection is bounded. v0 starts at
  **`TucanoBR/Tucano-630m`** (fits comfortably in T4 with room for batch),
  with **`TucanoBR/Tucano-1b1-Instruct`** as the v1 stretch target via
  QLoRA on Kaggle 2×T4. 7B is out of scope for v0/v1.

## 4. Frontend integration — **none**

- The `lyrics-llm` sub-project is independent of `index.html` / the static
  music player. They share the repo, nothing else.
- Implication: the v1 demo surface is just a local CLI / notebook / Ollama
  prompt — no JS, no API server, no UI work.

## Existing repo songs

- The 18 `songs/*.mp3` already in the repo do **not** have associated
  lyrics we can pull in. They are not seed data for this project.

## Implied base-model + tokenizer plan

- **v0 base:** `TucanoBR/Tucano-630m` (Apache-2.0, pt-native tokenizer — no
  vocab work needed).
- **v1 base:** `TucanoBR/Tucano-1b1-Instruct` if v0 results justify it.
- **Fallback baseline for comparison:** `rsmonteiro/gpt2-small-portuguese-lyrics`
  (existing prior-art lyrics fine-tune). Useful to sanity-check our pipeline
  against an existing pt lyrics model.
- **Tokenizer:** keep Tucano's as-is. Add structural special tokens
  (`<verso>`, `<refrão>`, `<ponte>`) before training.

## What this rules out

- Sabiá-7B (research-only license, 7B is too big for free tier).
- Bode-7B / 13B (size).
- Llama-3-8B / Mistral-7B with vocab extension (size + the vocab work itself
  costs compute we don't have).
- Pan-genre dataset construction (we are deliberately narrow).
- A web demo bolted onto the music player.
