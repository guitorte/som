# Frontier-LLM alternative path

Companion to [`01-field-notes.md`](./01-field-notes.md). That doc surveys
how lyric generation is *normally* tackled (dedicated fine-tune). This one
maps how a frontier instruction-following LLM — e.g. Claude Opus 4.7 — can
do the same job by planning, self-critiquing, and using tools, and how a
hybrid plan could combine the two.

---

## TL;DR — three tracks

- **Track A — Dedicated fine-tune.** What [`ROADMAP.md`](../ROADMAP.md)
  already describes. Scrape sertanejo, fine-tune Tucano, run locally.
  Slow, fiddly, build-it-yourself, fully independent.
- **Track B — Agentic Claude orchestrator.** Drive Claude through explicit
  planning, in-context rhyme dictionaries, syllable-counter tool calls,
  and a generate-critique-revise loop. No training, no scraping.
  Probably outperforms Track A's v0 from day one.
- **Hybrid.** Use Track B to *generate* a 5k synthetic sertanejo corpus
  with structure markers, then fine-tune Tucano on **that**. Sidesteps
  Vagalume entirely; produces a local model whose ceiling is shaped by
  Claude.

---

## The reframe

The issues in [`01-field-notes.md`](./01-field-notes.md) — non-local rhyme,
tokenization vs. phonology, copyrighted training data, no canonical eval,
long-form coherence — are framed around the limits of a small autoregressive
LM that must do form + content + fluency in a single left-to-right pass with
no scratchpad and no external check.

A frontier LLM doesn't carry those limits. It can:

- **Plan before writing** — pick rhyme words first, then write to them.
- **Use a scratchpad** — extended thinking, structured reasoning.
- **Use tools** — call a Python syllable counter and revise.
- **Self-critique** — score its own output and rewrite the weak parts.
- **Work in passes** — outline → fill → polish → verbatim-check.

Almost every issue gets a leverage point that does not exist for a 2B
fine-tune.

---

## Per-issue mitigations

| Issue | Track A handles it by | Track B handles it by |
|---|---|---|
| Form vs L2R LM | Pasini's prepend-rhyme reordering | Plan rhyme words first in the prompt |
| Rhyme is non-local | Reverse / prepend reordering at train time | Pre-generate rhyme dictionary in context |
| Tokenization vs phonology | Syllable-aware tokenizer (defer to v2) | Phonemes/IPA in chain-of-thought |
| Copyrighted training data | Scrape research-only, keep local | No training corpus needed; verbatim-check post-hoc |
| No canonical eval | Roll-our-own metric stack | Claude-as-judge over 5 variants |
| Memorization risk | Dedup, training-time noise | Lower base rate; verbatim check |
| Long-form coherence | Plan-then-write at SFT time | Multi-pass outline → fill → polish |

---

## Concrete agentic patterns (in cost order)

1. **Single-prompt structured CoT.** "First output: (a) sub-genre markers,
   (b) rhyme scheme, (c) rhyme word per line, (d) syllable budget per line.
   Then write." One call. ~70% of the gains.
2. **Retrieve-then-write.** Two calls. Claude generates a sertanejo rhyme
   dictionary + idiom list for the requested theme; the writing prompt
   consumes them.
3. **Generate-critique-revise loop.** Three roles, N iterations. Lyricist
   writes; critic scores line-by-line on rhyme, meter, sub-genre fit;
   reviser fixes low-scoring lines. The Claude Agent SDK fits this natively.
4. **Tool-augmented verification.** Give Claude `count_syllables(line)` and
   `rhymes_with(a, b)` tools (pyphen + pt phonetic last-syllable). After
   each line the model calls them and revises if it missed. This is where
   prompt-engineering *beats* a small fine-tune — no fine-tune consults an
   oracle.
5. **Variant juries.** Generate 5 candidates in parallel; a jury Claude
   call ranks them; the runner-up is rewritten against the jury's
   objections.
6. **Few-shot style anchoring.** 3-5 sertanejo excerpts in the prompt
   (paraphrased to dodge copyright concerns) sharpen sub-genre fit. Cheap;
   probably the single biggest quality lever.
7. **Reverse-order line composition.** "Write line 2 ending with `coração`
   first. Now write line 1 leading into it." Prompt-level emulation of
   reverse language modeling.

---

## Track comparison

| Dimension | Track A — SFT | Track B — Claude | Hybrid |
|---|---|---|---|
| Time to v0 | 1-2 weeks | hours | 1-2 weeks |
| Per-generation cost | free (local) | ~$0.01-0.10 / lyric | free after training |
| Per-generation latency | < 1s | 5-30s | < 1s |
| Stylistic depth | high once corpus is good | bounded by Claude's pt-BR / sertanejo knowledge | both |
| Data licensing risk | high (scraped) | none (no training corpus) | none (synthetic only) |
| Build-it-yourself learning | very high | medium | very high |
| Quality ceiling | base model + corpus | Claude | Claude × local |
| Independence at inference | full | none (API) | full |

---

## The Hybrid path in detail

If Hybrid is chosen, the sequence is:

### Phase H1 — Synthetic corpus generation (3-5 days)

Build `scripts/synth_corpus.py` that drives the Claude API through the
agentic patterns above to generate ~5k labeled sertanejo lyrics, schema:

```json
{
  "id": "synth-00001",
  "sub_genre": "sofrencia",
  "theme": "boteco depois do termino",
  "structure": ["verso", "verso", "refrao", "verso", "refrao", "ponte", "refrao"],
  "rhyme_scheme": "AABB",
  "lyrics": "<song><verso>... <refrao>... </song>"
}
```

Stratified across raiz / universitário / sofrência / feminejo (~1.25k each).

### Phase H2 — Quality filter

Self-score every generation with a jury Claude call on `{rhyme accuracy,
syllable compliance, sub-genre fit, coherence, originality}`. Drop the
bottom 20%. Keep the top 80% as the SFT training set.

### Phase H3 — SFT on Tucano (= Track A Phase 4)

Same QLoRA recipe, synthetic corpus instead of scraped data. Apache-2.0
training data, Apache-2.0 base model — clean licensing posture.

### Phase H4 — Eval (= Track A Phase 5)

Compare the Hybrid checkpoint to:

- Zero-shot Tucano-630m (Phase 0 baseline).
- Direct Claude (Track B at inference).
- Track A's scraped-data fine-tune, if we ever build one.

---

## Costs

Rough Claude API budget for 5k lyrics with extended thinking + critique
loop, averaging ~8k output tokens per song at Opus 4.7 list pricing:

- ~$150 one-time for corpus generation.
- ~$5-10 for the jury filtering pass.

If the user opts into the Hybrid path, this is a one-shot personal-budget
question, not an ongoing cost. After training, inference is free / local.

---

## Open decisions

1. **Which track?** A only / B only / Hybrid — see ROADMAP for stub phases.
2. **If Hybrid:** OK to spend ~$150 on Claude API for corpus generation?
3. **If B at inference:** Claude API directly, OpenRouter, or local
   Llama/Qwen via Ollama as a cheaper proxy?
4. **Track simultaneity:** keep all three alive in the roadmap, or commit
   to one and delete the others?
