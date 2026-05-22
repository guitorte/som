# evaluation/

Tooling for measuring lyric-generation quality across the project's
checkpoints.

## What's here now

- `prompts/sertanejo_prompts.json` — 20 sertanejo prompts (5 per sub-genre:
  raiz / universitário / sofrência / feminejo). Used by Phase 0 zero-shot
  eval and reused as a regression set in later phases.

## What goes here later (per ROADMAP Phase 5)

- `perplexity.py` — held-out perplexity on `test.parquet`.
- `syllables.py` — per-line syllable count via `syllable-pt` + Pyphen.
- `rhyme.py` — end-rhyme accuracy via pt phonetic last-syllable matching.
- `bertscore.py` — BERTScore vs reference lyrics (backbone: BERTimbau base).
- `self_eval.md` — personal 1-5 Likert protocol.
- `run.py` — orchestrator, emits `eval_report.md`.

## Prompt set design notes

- 5 prompts × 4 sub-genres so we can compare per-sub-genre fit, not just
  overall.
- Each prompt names the sub-genre explicitly to anchor the model. Once we
  add `<sub-gênero=X>` special tokens after fine-tuning, drop the genre
  word from the prompt body and rely on the tag.
- All prompts end with `\n\n` so the model continues on a new line rather
  than completing the prompt sentence inline.
- The set is small on purpose. It's a regression suite, not a benchmark —
  if it grows past ~50 we should split off a held-out test set.
