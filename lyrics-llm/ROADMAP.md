# Roadmap — pt-BR Lyrics LLM

**Status:** first draft, 2026-05-22. Open to revision after Phase 0 review.

Companion docs: [`README.md`](./README.md), [`REFERENCES.md`](./REFERENCES.md).

---

## Guiding decisions to make first

Before any training code runs, four upstream choices set the rest of the plan:

1. **Use-case.** Personal/research toy vs. public demo vs. production. This
   decides everything downstream — especially data licensing.
2. **Genre scope.** Pan-pt-BR ("any lyric") vs. specific genre (sertanejo,
   funk, MPB, trap, gospel, samba). Narrower = smaller dataset works.
3. **Conditioning surface.** Pure free-form generation vs. conditional on
   `{genre, mood, seed line, rhyme scheme, syllable count}`. Conditional needs
   metadata-rich training data.
4. **Compute budget.** Free Colab/Kaggle only vs. ~$50 on RunPod vs.
   serious training. This decides base-model size.

**Default working assumption** (revisit after Phase 0): research/toy project,
pan-genre with optional genre conditioning, free-form generation with simple
controls, budget ≤ $50.

---

## Phase 0 — Scope & feasibility (1-2 days)

**Goal:** lock the four decisions above and confirm the project is buildable
with available resources.

- [ ] Pick the four upstream choices.
- [ ] Decide license posture: research-only, no commercial use, no model
      weights redistributing unmodified copyrighted lyrics.
- [ ] Pick the base-model candidate set (default: `TucanoBR/Tucano-1b1-Instruct`,
      `TucanoBR/Tucano-2b4-Instruct`, optional `maritaca-ai/sabia-7b`).
- [ ] Sanity-load each candidate, generate ~20 free-form prompts, log
      qualitative pt fluency and lyric-likeness.
- [ ] Write a one-pager `docs/00-scope.md` capturing the decisions.

**Exit criteria.** A decision document committed. A short
"can-the-base-model-do-this-zero-shot?" report in `docs/`.

---

## Phase 1 — Data acquisition (3-5 days)

**Goal:** assemble a clean, deduplicated pt-BR lyrics corpus of 10k-50k songs
with at minimum `{title, artist, genre, lyrics}` per row.

- [ ] Pick scraping sources: **Vagalume API** primary (lawful via API key);
      4MuLA secondary (research only, redistribution unclear); letras.mus.br
      only if other paths fail and only for personal use.
- [ ] Apply for a Vagalume API key. Document rate limits and ToS in
      `docs/01-data-sources.md`.
- [ ] Write `scripts/scrape_vagalume.py` — paginated, polite (≥1s between
      requests), resumable, writes JSONL to `data/raw/` (gitignored).
- [ ] Optional: pull 4MuLA Tiny from Zenodo as a head-start.
- [ ] Collect genre/mood metadata where available; this is the conditioning
      signal later.

**Exit criteria.** `data/raw/lyrics.jsonl` with ≥ 10k rows;
`docs/01-data-sources.md` documenting provenance and license posture per source.

---

## Phase 2 — Data cleaning & preprocessing (2-3 days)

**Goal:** turn raw scrapes into a training-ready, deduplicated corpus.

- [ ] `scripts/clean.py`: strip HTML, normalize Unicode (NFC), collapse
      whitespace, fix smart-quotes, expose section markers (verse/chorus/bridge)
      as structural tokens (`<verso>`, `<refrão>`, `<ponte>`).
- [ ] Language ID with `fasttext` or `lingua-py`; drop non-pt rows.
- [ ] Near-duplicate detection: MinHash on shingles, drop ≥0.85 Jaccard
      duplicates (cover versions, re-uploads).
- [ ] Profanity / explicit handling: tag with `[explicit]` rather than filter
      (preserves stylistic variety). Decision can be revisited.
- [ ] Train/val/test split (90/5/5) — **stratified by artist** to prevent
      artist leakage between splits.
- [ ] Persist as Parquet under `data/processed/` (gitignored). Schema:
      `id, title, artist, genre, year, lyrics, lines, n_lines, n_chars, n_syllables, hash`.

**Exit criteria.** `data/processed/{train,val,test}.parquet`; a one-page
data card in `docs/02-data-card.md`.

---

## Phase 3 — Tokenizer / vocab decisions (1-2 days)

**Goal:** make sure the tokenizer doesn't sabotage pt-BR generation.

- [ ] Measure tokens-per-byte on the corpus for each base-model tokenizer.
      Tucano tokenizer is expected to win; Llama/Mistral will fragment.
- [ ] Decision branch:
    - If using **Tucano**: keep tokenizer as-is.
    - If using **Llama/Mistral base**: either (a) accept fragmentation for v1
      and revisit, or (b) train a 32k Unigram SentencePiece on the lyrics
      corpus and merge with the base vocab (DeBERTinha-style).
- [ ] Add special tokens: `<song>`, `<verso>`, `<refrão>`, `<ponte>`,
      `<gênero=X>`, `<sílabas=N>` if conditioning will use them.

**Exit criteria.** A short `docs/03-tokenizer.md` with the chosen approach
and the tokens-per-byte numbers.

---

## Phase 4 — Baseline fine-tune (2-4 days)

**Goal:** a small model that demonstrably writes lyric-shaped pt-BR text.

- [ ] Pick `TucanoBR/Tucano-1b1-Instruct` as default starting point.
- [ ] Fine-tune via **QLoRA / Unsloth** on a single 24GB GPU (RunPod) or
      Kaggle 2×T4. Use TRL's `SFTTrainer` with packing.
- [ ] Training data format: instruction-style with the optional control
      tokens, e.g.

  ```text
  <song><gênero=sertanejo>Escreva uma música sobre saudade da roça.</s>
  <verso>...
  <refrão>...
  </song>
  ```

- [ ] Hyperparameters (starting point, expect to tune):
      `lr=2e-4`, `batch=4` × `grad_accum=8`, `epochs=2-3`, `lora_r=16`,
      `lora_alpha=32`, `lora_target_modules=q,k,v,o,gate,up,down`,
      `bf16`, `max_seq_len=2048`.
- [ ] Log to `wandb` or `tensorboard`.
- [ ] Save adapter to `data/adapters/v1/` (gitignored); merge to BF16 for eval.

**Exit criteria.** A merged checkpoint that beats the zero-shot base on
held-out perplexity by ≥10%, with qualitatively lyric-shaped samples.

---

## Phase 5 — Evaluation harness (parallel with Phase 4, 2-3 days)

**Goal:** quantitative and qualitative measurement that actually tracks
song-craft, not just perplexity.

- [ ] `evaluation/perplexity.py` — perplexity on `test.parquet`.
- [ ] `evaluation/syllables.py` — per-line syllable count using
      `syllable-pt` + `Pyphen` ensemble. Output: distribution + compliance
      vs. target if conditioning was used.
- [ ] `evaluation/rhyme.py` — extract last stressed-syllable phoneme; compute
      end-rhyme accuracy across paired lines (AABB, ABAB schemes).
- [ ] `evaluation/bertscore.py` — BERTScore vs. references, backbone =
      `neuralmind/bert-large-portuguese-cased`.
- [ ] `evaluation/human_eval.md` — protocol for ~50-song side-by-side
      eval by Brazilian speakers on `{grammaticality, poeticness, genre fit,
      coherence}` 1-5 Likert. Use a Google Form.
- [ ] Roll up into a single `evaluation/run.py` that emits `eval_report.md`.

**Exit criteria.** `eval_report.md` for v1 checkpoint vs. base.

---

## Phase 6 — Controllability & iteration (open-ended)

Pick from these once v1 is shipped:

- **Genre conditioning.** Already implicit via `<gênero=X>`; sweep genres,
  measure per-genre coherence.
- **Rhyme-aware generation.** Implement Pasini et al. 2024's prepend-rhyme
  trick (arXiv 2405.05176) or DeepRapper-style reverse-order generation.
- **Syllable control.** Inject `<sílabas=N>` tokens at line start and
  train on counts derived from the cleaning step. Decode with a syllable-budget
  constrainer.
- **Song structure control.** Plan-then-write: have the model first emit a
  structure (`verso, verso, refrão, verso, refrão, ponte, refrão`) and then
  fill it in.
- **DPO / preference tuning.** Pair model outputs with human Likert scores;
  train DPO to push fluency/poeticness.
- **Scale up.** Repeat with Tucano-2b4-Instruct, then Sabiá-7B (research-only)
  or Llama-3-8B (with tokenizer extension).

---

## Phase 7 — Deployment & demo (1-2 days, once happy with v1)

- [ ] Merge adapter → BF16 → convert to GGUF Q4_K_M / Q5_K_M.
- [ ] Publish quantized model to a private HF repo (do **not** publish a
      model that reproduces copyrighted lyrics verbatim).
- [ ] Local demo path: Ollama `Modelfile` with a default lyric-writing system
      prompt. Optional vLLM endpoint if multi-user demos are needed.
- [ ] Integrate with the existing static music-player frontend in this repo:
      add a "compose new lyric" button that POSTs a prompt to a local Ollama
      endpoint and renders the result alongside an existing song.

**Exit criteria.** A two-command local demo (`ollama pull` → `ollama run`)
that generates a pt-BR lyric on prompt, served behind the existing
`index.html`.

---

## Risk register

| Risk | Likelihood | Mitigation |
|---|---|---|
| Lyrics copyright blocks commercial use | High | Stay research-only; never redistribute training data; model card warns on commercial deployment. |
| Vagalume API rate-limits or revokes key | Medium | Polite scraping, cache aggressively, fall back to 4MuLA. |
| Tokenizer over-fragments pt | Medium | Default to Tucano family which avoids it. |
| Memorization of full copyrighted lyrics | Medium | Dedup training data, test for verbatim regurgitation in eval, apply training-time noise (line shuffling within sections). |
| Evaluation drift (no pt lyric benchmark) | High | Document our home-grown stack as v1, version it, share eval scripts so results are reproducible. |
| Genre imbalance | High | Stratified eval, oversample under-represented genres in later iterations. |
| Compute budget overrun | Low | Start at 1B params; scale only after eval gains justify it. |

---

## Open questions (please weigh in)

1. **Use-case** — toy/research only, or eventual public demo?
2. **Genre** — pan-genre or pick a focus (e.g., sertanejo)?
3. **Compute** — happy with free Colab/Kaggle for v1, or pre-approved to spend
   ~$20-50 on RunPod for a faster loop?
4. **Frontend integration** — should the existing music-player `index.html`
   gain a "compose lyric" button as the project's demo surface, or do we
   keep the LLM work standalone?
5. **Songs in this repo** — the 18 `songs/*.mp3` already here suggest a
   personal/local corpus. Are the corresponding lyrics available somewhere
   we can pull in as seed data?
