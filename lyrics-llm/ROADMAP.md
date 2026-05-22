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

## Approach tracks

There are three viable paths to the locked goal. See
[`docs/02-frontier-llm-alt-path.md`](./docs/02-frontier-llm-alt-path.md) for
the full comparison.

- **Track A — Dedicated fine-tune.** Phases 0-7 below. Scrape sertanejo
  lyrics → fine-tune Tucano → local inference. Slow, self-contained, the
  "build it yourself" path.
- **Track B — Agentic Claude orchestrator.** Phases B0-B3 further down.
  No training; drive Claude Opus through plan → rhyme dictionary → write
  → critique → revise → syllable-tool verify. Days, not weeks.
- **Hybrid — Track B feeds Track A.** Phases H1-H4. Use Claude to generate
  a 5k synthetic sertanejo corpus, then fine-tune Tucano on that. Clean
  licensing, local at inference, but adds a one-time ~$150 Claude-API
  budget.

**Current status:** Track A is scaffolded through Phase 0 (see below).
Tracks B and Hybrid are roadmap stubs — pick whether to pursue one before
writing code under them.

---

# Track A — Dedicated fine-tune

## Phase 0 — Feasibility check (½-1 day) — scaffolded, awaiting run

Scope locked in [`docs/00-scope.md`](./docs/00-scope.md). Scaffolding for the
feasibility run is in:

- [`scripts/zero_shot.py`](./scripts/zero_shot.py) — model-agnostic runner.
- [`evaluation/prompts/sertanejo_prompts.json`](./evaluation/prompts/sertanejo_prompts.json) — 20 prompts (5 × 4 sub-genres).
- [`notebooks/00_zero_shot_sertanejo.ipynb`](./notebooks/00_zero_shot_sertanejo.ipynb) — Colab T4 runner.
- [`docs/00-zero-shot-samples.md`](./docs/00-zero-shot-samples.md) — verdict template.

Tasks:

- [x] Lock scope decisions.
- [x] Scaffold prompts + runner + Colab notebook + verdict template.
- [ ] Open the notebook in Colab T4, run all cells. Generates ~60 samples
      (20 prompts × 3 models) in ~10-15 min.
- [ ] Commit the three result JSONs back to the branch.
- [ ] Fill `docs/00-zero-shot-samples.md` with the verdict: confirm Tucano-630m
      as v0, or escalate to 1b1 / step down to 160m.

**Exit criteria.** `docs/00-zero-shot-samples.md` filled in with a chosen
v0 base model.

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

# Track B — Agentic Claude orchestrator

No training, no scraping. Drive Claude Opus 4.7 through structured
prompting and tool use. See [`docs/02-frontier-llm-alt-path.md`](./docs/02-frontier-llm-alt-path.md)
for the agentic patterns referenced below.

## Phase B0 — Decide on the API surface (½ day)

- [ ] Pick the LLM: Claude Opus 4.7 (default), Claude Sonnet 4.6 (cheaper
      fallback), or a local Qwen2.5-72B-Instruct via Ollama (zero API cost
      but slower).
- [ ] Pick the auth path: direct Anthropic API key vs OpenRouter.
- [ ] Commit a `.env.example` (not the key itself) under `configs/`.

## Phase B1 — `compose.py` orchestrator (2-3 days)

Build a single CLI that takes `--sub-gênero` and `--tema` and produces a
sertanejo lyric via the agentic loop. Pattern (in increasing complexity,
ship the simplest one that works):

1. **Single-prompt structured CoT.** One call: plan + rhyme words + lyric.
2. **Two-call retrieve-then-write.** First call generates a rhyme
   dictionary and idiom list; second call writes against it.
3. **Critique-revise loop.** Add a critic call that scores rhyme / meter /
   sub-genre fit per line; reviser fixes anything below threshold; loop
   up to N iterations.

Acceptance: 20/20 of the Phase 0 sertanejo prompts produce a coherent
sertanejo lyric on first run.

## Phase B2 — Syllable / rhyme tool wiring (1-2 days)

- [ ] Implement `count_syllables(line)` via `pyphen` + `syllable-pt`
      ensemble (matches Phase 5 evaluation tooling — share the code).
- [ ] Implement `rhymes_with(word_a, word_b)` via pt phonetic last-syllable
      match.
- [ ] Expose both as Claude tools; have `compose.py` register them.
- [ ] Verify the model actually calls them and revises on failure.

## Phase B3 — Quality eval on Track B (1 day)

- [ ] Reuse the Phase 5 metric harness against Track B outputs across the
      20 sertanejo prompts. Numbers go in `docs/B3-track-b-eval.md`.
- [ ] If Track B already exceeds quality targets, the hybrid path is
      unlocked (use these outputs as synthetic training data).

---

# Hybrid — Track B feeds Track A

Use Track B as a synthetic-data generator for Track A. Sidesteps the
Vagalume scrape entirely and gives clean licensing.

## Phase H1 — Synthetic corpus generation (3-5 days + API spend)

- [ ] Decide on corpus size and budget. Default: 5k lyrics × ~$0.03 each
      ≈ $150 with Opus 4.7. Could be 2k × Sonnet 4.6 if cheaper.
- [ ] Extend `compose.py` into `scripts/synth_corpus.py` that loops over
      `(sub_genre, theme)` pairs and writes JSONL to `data/synthetic/`.
- [ ] Stratify themes across raiz / universitário / sofrência / feminejo
      so each sub-genre gets ~1.25k lyrics.
- [ ] Persist per-row metadata: `{id, sub_genre, theme, structure,
      rhyme_scheme, lyrics, claude_self_score}`.

## Phase H2 — Quality filter (½ day)

- [ ] Jury Claude pass over every row: score on `{rhyme accuracy,
      syllable compliance, sub-genre fit, coherence, originality}` 1-5.
- [ ] Drop the bottom 20%. Document the cutoff in `docs/H2-filter.md`.

## Phase H3 — SFT on Tucano (= Track A Phase 4 with synthetic data)

Same QLoRA recipe as Track A Phase 4, just pointing at
`data/synthetic/train.parquet` instead of `data/processed/train.parquet`.
Licensing posture is clean: Apache-2.0 training data, Apache-2.0 base.

## Phase H4 — Comparative eval (1 day)

- [ ] Run the Phase 5 harness against three checkpoints side by side:
      zero-shot Tucano, Hybrid-fine-tune, Track B direct (Claude).
- [ ] If Hybrid local-inference beats Track B direct on enough samples,
      the project ships locally without ongoing API cost.

---

## Risk register (post scope-lock)

| Risk | Track | Likelihood | Mitigation |
|---|---|---|---|
| Vagalume API rate-limits or revokes key | A | Medium | Polite scraping, cache aggressively, fall back to 4MuLA Tiny; or pivot to Hybrid. |
| Free-tier session timeouts kill long runs | A, Hybrid | High | Checkpoint every N steps; resumable training; keep epochs short on 630m. |
| Kaggle 2×T4 OOM on 1b1 QLoRA | A, Hybrid | Medium | Use `max_seq_len=1024`, gradient checkpointing, paged AdamW; if still OOM, stay on 630m. |
| Memorization of training lyrics | A | Medium | Dedup, test for verbatim regurgitation; personal-use scope contains downstream impact. |
| Sertanejo sub-genre imbalance | A, Hybrid | Medium | Stratified eval; oversample weak sub-genres if v0 shows skew. |
| Evaluation drift (no pt lyric benchmark) | All | High | Roll our own metric stack, version it; reuse across all checkpoints. |
| Lyrics copyright (training data) | A | Low (personal scope) | Keep raw corpus out of git; do not publish model weights publicly. |
| Claude API spend overruns | B, Hybrid | Low | Set a hard budget cap in `compose.py`; default to Sonnet 4.6 for bulk generation. |
| Claude rate limits during synthetic generation | Hybrid | Low | Stream incrementally to JSONL; resumable; can run overnight. |
| Track B has external dependency at inference | B | High | If independence matters, fall back to Hybrid (local at inference). |
