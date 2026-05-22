# Roadmap — pt-BR Lyrics LLM

**Status:** first draft, 2026-05-22. Open to revision after Phase 0 review.

Companion docs: [`README.md`](./README.md), [`REFERENCES.md`](./REFERENCES.md).

---

## Locked scope (v0 — see `docs/00-scope.md`)

1. **Use-case** — personal only. No public demo, no commercial use, no
   model weight publishing.
2. **Genre** — **sertanejo** (raiz, universitário, sofrência, feminejo).
3. **Compute** — free tier only (Colab T4, Kaggle 2×T4).
4. **Frontend** — none. The sub-project is independent of `index.html`.

Implications baked into every phase below:

- **Base model: `TucanoBR/Tucano-630m`** for v0, optional bump to
  `TucanoBR/Tucano-1b1-Instruct` for v1. 7B is out of scope.
- **Corpus target:** ~5k-15k sertanejo songs (genre-focused → smaller is fine).
- **Tokenizer:** keep Tucano's, add structural special tokens, no vocab extension.
- **No `index.html` integration**; demo surface is a local CLI / Ollama prompt.

---

## Phase 0 — Feasibility check (½-1 day) ✓ scope locked

Scope is locked in `docs/00-scope.md`. What's left in Phase 0 is just
confirming the chosen base model handles sertanejo zero-shot at a level
worth fine-tuning from.

- [x] Lock scope decisions.
- [ ] On a Colab T4, load `TucanoBR/Tucano-630m` and `Tucano-1b1-Instruct`.
- [ ] Run ~20 sertanejo-flavored prompts (e.g., "Escreva uma música
      sertaneja sobre uma traição na fazenda…"). Capture outputs in
      `docs/00-zero-shot-samples.md`.
- [ ] For comparison, run the same prompts through
      `rsmonteiro/gpt2-small-portuguese-lyrics`.
- [ ] Verdict: confirm Tucano-630m is the right v0 starting point, or
      escalate to 1b1 / step down to 160m if memory/quality dictates.

**Exit criteria.** A short qualitative report committed under `docs/`.

---

## Phase 1 — Sertanejo data acquisition (3-5 days)

**Goal:** assemble a clean, deduplicated **sertanejo** corpus of 5k-15k songs
with `{title, artist, sub-genre, lyrics, year?}` per row. Personal-use only,
no redistribution.

- [ ] Build an artist seed list (~150-300 sertanejo artists across raiz,
      universitário, sofrência, feminejo). Anchors: Chitãozinho & Xororó,
      Leandro & Leonardo, Zezé Di Camargo & Luciano, Bruno & Marrone,
      Almir Sater, Sérgio Reis, Jorge & Mateus, Henrique & Juliano,
      Gusttavo Lima, Marília Mendonça, Maiara & Maraisa, Ana Castela,
      Simone Mendes, etc. Persist as `data/seed_artists.json`.
- [ ] **Primary source: Vagalume API.** Apply for a key. Document rate
      limits / ToS in `docs/01-data-sources.md`. Vagalume's genre taxonomy
      includes "sertanejo" — filter on it.
- [ ] **Secondary: 4MuLA Tiny (Zenodo).** Pull and filter rows where
      `genre == sertanejo`.
- [ ] Write `scripts/scrape_vagalume.py` — paginated, polite (≥1s between
      requests), resumable, writes JSONL to `data/raw/` (gitignored).
- [ ] Collect metadata: sub-genre tags, year, duo-vs-solo, region if
      available. These become later conditioning signals.

**Exit criteria.** `data/raw/sertanejo.jsonl` with ≥ 5k rows;
`docs/01-data-sources.md` documenting provenance and personal-use posture.

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

## Phase 3 — Tokenizer & special tokens (½ day)

Locked-scope choice (Tucano base) collapses this phase to adding structural
special tokens; no vocab extension required.

- [ ] Sanity-check tokens-per-byte of Tucano's tokenizer on the cleaned
      sertanejo corpus. Record in `docs/03-tokenizer.md`.
- [ ] Add special tokens to the tokenizer and resize model embeddings:
      `<song>`, `</song>`, `<verso>`, `<refrão>`, `<ponte>`,
      `<sub-gênero=X>` (raiz / universitário / sofrência / feminejo).
- [ ] Save the extended tokenizer locally; reuse it across all training runs.

**Exit criteria.** `docs/03-tokenizer.md` with TPB numbers and the special
token list.

---

## Phase 4 — Baseline fine-tune on sertanejo (2-4 days)

**Goal:** a small model that demonstrably writes sertanejo-shaped pt-BR text.

- [ ] **Base: `TucanoBR/Tucano-630m`** (v0). Optional bump to `Tucano-1b1-Instruct`
      for v1 once v0 trains end-to-end on Kaggle 2×T4.
- [ ] Fine-tune via **Unsloth QLoRA** on Kaggle 2×T4 (Colab T4 OK for 630m
      experiments). Use TRL's `SFTTrainer` with packing.
- [ ] Training data format: instruction-style with control tokens, e.g.

  ```text
  <song><sub-gênero=sofrência>Escreva uma música sertaneja sobre traição num boteco.</s>
  <verso>...
  <refrão>...
  </song>
  ```

- [ ] Hyperparameters (starting point, expect to tune):
      `lr=2e-4`, `batch=4` × `grad_accum=8`, `epochs=2-3`, `lora_r=16`,
      `lora_alpha=32`, `lora_target_modules=q,k,v,o,gate,up,down`,
      `bf16` (or `fp16` if T4 doesn't bf16), `max_seq_len=1024` to fit T4.
- [ ] Log to tensorboard (wandb optional; keep keys out of free-tier
      notebooks).
- [ ] Save adapter to `data/adapters/v0/` (gitignored); merge to FP16 for eval.

**Exit criteria.** A merged 630m checkpoint that beats the zero-shot base on
held-out perplexity by ≥10%, with qualitatively sertanejo-shaped samples.

---

## Phase 5 — Evaluation harness (parallel with Phase 4, 1-2 days)

**Goal:** quantitative and qualitative measurement that tracks sertanejo
song-craft, not just perplexity. Scaled down for personal-use scope.

- [ ] `evaluation/perplexity.py` — perplexity on `test.parquet`.
- [ ] `evaluation/syllables.py` — per-line syllable count using
      `syllable-pt` + `Pyphen` ensemble. Sertanejo verses are usually
      7-12 syllables (redondilha maior is common); flag drift.
- [ ] `evaluation/rhyme.py` — extract last stressed-syllable phoneme; compute
      end-rhyme accuracy. Sertanejo skews heavily AABB / AABB-with-refrain,
      so rhyme density is a strong genre-fit signal.
- [ ] `evaluation/bertscore.py` — BERTScore vs. references, backbone =
      `neuralmind/bert-base-portuguese-cased` (base for free-tier RAM).
- [ ] `evaluation/self_eval.md` — personal evaluation protocol: 20 generated
      lyrics scored 1-5 on `{grammaticality, sertanejo fit, coherence,
      tropes used}`. No external survey needed since this is personal-use.
- [ ] Roll up into `evaluation/run.py` that emits `eval_report.md`.

**Exit criteria.** `eval_report.md` for v0 checkpoint vs. base.

---

## Phase 6 — Controllability & iteration (open-ended)

Pick from these once v0 is shipped, in roughly increasing complexity:

- **Sub-genre conditioning.** Already implicit via `<sub-gênero=X>`; sweep
  sub-genres, measure per-sub-genre coherence.
- **Rhyme-aware generation.** Pasini et al. 2024's prepend-rhyme trick
  (arXiv 2405.05176) — strong fit because sertanejo is AABB-heavy.
- **Syllable control.** Inject `<sílabas=N>` tokens at line start and
  train on counts derived from the cleaning step. Decode with a
  syllable-budget constrainer.
- **Song structure control.** Plan-then-write: model first emits a structure
  (`verso, verso, refrão, verso, refrão, ponte, refrão`) and then fills it in.
- **v1 scale-up.** Repeat with `TucanoBR/Tucano-1b1-Instruct` if Kaggle
  2×T4 holds. 7B remains out of scope.
- **DPO from self-ratings.** Pair model outputs with personal Likert scores
  and train a small DPO pass.

---

## Phase 7 — Local personal use (½ day, once happy with v0)

Scope is personal-only, so this collapses to a local CLI workflow. No public
endpoints, no model weight publishing.

- [ ] Merge adapter → FP16 → convert to GGUF Q4_K_M with
      `llama.cpp/convert_hf_to_gguf.py`.
- [ ] Wire up an Ollama `Modelfile` that bakes in a sertanejo-flavored system
      prompt and the special tokens.
- [ ] `scripts/compose.py` — one-shot CLI: `python scripts/compose.py --sub raiz --tema "saudade da fazenda"`
      → prints a generated lyric.
- [ ] Optional: keep the GGUF and adapter in a local private HF repo for
      personal backup (private only — no public weights given training-data
      origin).

**Exit criteria.** `ollama run sertanejo-llm` produces a lyric on prompt
from a local terminal.

---

## Risk register (post scope-lock)

| Risk | Likelihood | Mitigation |
|---|---|---|
| Vagalume API rate-limits or revokes key | Medium | Polite scraping, cache aggressively, fall back to 4MuLA Tiny. |
| Free-tier session timeouts kill long runs | High | Checkpoint every N steps; resumable training; keep epochs short on 630m. |
| Kaggle 2×T4 OOM on 1b1 QLoRA | Medium | Use `max_seq_len=1024`, gradient checkpointing, paged AdamW; if still OOM, stay on 630m. |
| Memorization of training lyrics | Medium | Dedup, test for verbatim regurgitation in eval; personal-use scope contains downstream impact. |
| Sertanejo sub-genre imbalance (e.g., feminejo under-represented) | Medium | Stratified eval; oversample weak sub-genres if v0 shows skew. |
| Evaluation drift (no pt lyric benchmark) | High | Roll our own metric stack, version it; reuse across all checkpoints. |
| Lyrics copyright (training data) | Low (personal scope) | Keep raw corpus out of git; do not publish model weights publicly. |
