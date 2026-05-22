# Field notes — state of AI lyric/poetry generation (May 2026)

Synthesis of the research collected in [`REFERENCES.md`](../REFERENCES.md),
written so the next session doesn't have to rebuild this context from chat
history. Treat this as the "why we made the roadmap choices we made"
companion to [`00-scope.md`](./00-scope.md) and [`ROADMAP.md`](../ROADMAP.md).

---

## 1. Why this is hard — the core tensions

**Form fights language modeling.** A standard LM is trained to predict the
most likely next token. Poetry/lyrics need the *last* word of each line to
satisfy rhyme and the *count* of syllables on each line to satisfy meter.
The most constrained decisions are exactly the ones a left-to-right
autoregressive model defers until last — by the time it commits to a line
ending, it has already painted itself into a corner.

**Rhyme is a non-local constraint.** To rhyme with `coração`, the line
being written must end on `-ão`. The model only learns to do that if either
(a) the architecture forces the decision early, or (b) the training data
is restructured so the model sees the constraint up-front.

**Tokenization fights phonology.** BPE/SentencePiece tokenizers split on
frequency, not pronunciation. `coração` and `violão` rhyme in pt-BR; they
may or may not share a token. The model has no built-in notion of phonetic
last-syllable equivalence — it has to learn it as an emergent statistical
pattern, and small models often don't.

**Lyrics are copyrighted.** Unlike news or Wikipedia, there is **no large
permissively licensed lyrics corpus**. Every dataset surveyed (4MuLA,
sheacon/song_lyrics, the Genius scrapes, the WASABI corpus) is research-only.
Brazil has no settled fair-use precedent for AI training, so commercial
deployment is effectively blocked without paying Musixmatch / LyricFind / ECAD.

**Evaluation has no canonical metric.** Perplexity ≠ "good lyric." BLEU/ROUGE
want reference matches, which fights creativity. Every paper invents its
own metric stack (rhyme accuracy + syllable compliance + BERTScore + small-N
human eval). There is no shared leaderboard, and results across papers are
not comparable.

**Memorization risk.** A model fit on ~1M copyrighted lyrics will sometimes
regurgitate verbatim — bad legally, bad creatively. DeepRapper and others
discuss this; the only known mitigations are aggressive deduplication and
training-time noise (line shuffling, paraphrasing).

**Coherence over song-length structure.** Songs have a thematic arc:
verse → chorus → bridge → chorus. A line-by-line LM handles surface fluency
but routinely loses the thread between sections; the chorus drifts off-topic.

---

## 2. How authors actually tackle it

The major patterns in the papers indexed in
[`REFERENCES.md` §4](../REFERENCES.md#4-academic-papers):

### A. Reverse language modeling — DeepRapper, DopeLearning

Train the model right-to-left so the rhyme word is generated first.
Solves rhyme directly but throws away pretrained LMs (must train from scratch)
and breaks tokenizer reuse. Largely superseded.

### B. Prepend-the-rhyme-word — Pasini et al. 2024 ([arXiv 2405.05176](https://arxiv.org/abs/2405.05176))

Clever middle path: reorder training data so each line starts with its
own last word. The model still generates left-to-right, but it commits to
the rhyme word *first*. Keeps pretrained-LM benefits, beats reverse-LM on
quality, and works across 13 languages. **This is the paper most directly
applicable to our project — schedule for v1 controllability.**

### C. Control codes / structural tokens — PoeLM, GPT Czech Poet, CTG survey ([arXiv 2408.12599](https://arxiv.org/abs/2408.12599))

Add special tokens: `<rhyme=ão>`, `<syllables=8>`, `<verso>`, `<refrão>`,
`<sub-gênero=sofrência>`. Train on data labeled with these tokens; prefix
prompts with the desired ones. Simple, plug-and-play with any LM, but soft —
the model "usually" respects the tag rather than guaranteeing it.

**This is what our v0 plan uses** (Phase 3 of the roadmap).

### D. Syllable-aware tokenization — GPT Czech Poet ([arXiv 2407.12790](https://arxiv.org/abs/2407.12790))

Tokenize at syllable or character granularity so the model can natively
count. Trade-off: 3-5× longer sequences, slower training, but rhyme + meter
improve sharply. Worth considering for pt-BR because pt syllable structure
is regular. Defer to v2.

### E. Forced / constrained decoding — Regex-Instruction ([arXiv 2309.10447](https://arxiv.org/abs/2309.10447))

Mask logits at decode time so only tokens that lead to a valid
syllable/rhyme constraint are allowed. Works mechanically; degrades fluency
because the unconstrained beam is fighting the constraint.

### F. Multi-stage / plan-then-write — SegTune, Song Form-aware T2L ([arXiv 2411.13100](https://arxiv.org/abs/2411.13100))

Generate a structural outline first (verse 1 theme, chorus theme, …),
then fill each section conditioned on the plan. Big wins on coherence at
modest cost (same model, two passes).

### G. Preference alignment — Raply ([arXiv 2407.06941](https://arxiv.org/abs/2407.06941)), JAM ([arXiv 2507.20880](https://arxiv.org/abs/2507.20880))

SFT → collect human ratings → DPO. Pushes "aesthetics" without architectural
changes. Standard last-mile polish in 2025-26 work.

### H. Continued pretraining + SFT — Sabiá, Tucano, Bode for pt

Not lyric-specific; this is just how anyone gets a halfway-decent pt LM.
Tucano's contribution is doing it *fully open* with the 200B-token GigaVerbo
corpus ([arXiv 2411.07854](https://arxiv.org/abs/2411.07854)).

Modern lyric papers combine 2-4 of these. Pasini's prepend-rhyme + control
codes + decode-time tweaks is roughly the current open-research recipe.

---

## 3. What's specific to pt-BR (and sertanejo)

- **Tucano is the only fully-open pt-native LM family.** Sabiá-7B is better
  at raw pt quality but LLaMA-1 research-only license blocks redistribution.
  Bode is Llama-2-derived (community license, OK for personal use).
- **Tokenizer drift is a real cost.** Llama/Mistral tokenize `saudade`,
  `coração`, common contractions like `pra`/`tá` into 3-4 fragments each.
  Tucano avoids this since it was pretrained from scratch with a pt vocabulary.
- **The closest pt lyrics work** is
  [`rsmonteiro/gpt2-small-portuguese-lyrics`](https://huggingface.co/rsmonteiro/gpt2-small-portuguese-lyrics)
  — a GPT-2 small (124M) fine-tune from **2022**. Five years stale. Nobody
  has visibly published an open pt lyrics LM since.
- **For sertanejo specifically: zero published open work.** Our project is
  plausibly the first dedicated open sertanejo LM. No SOTA to chase, but
  also no benchmark, no leaderboard, and no community baseline.
- **Sertanejo is unusually amenable to these techniques.** Heavy AABB
  rhyming, redondilha-maior syllable counts (7+1 or 10+1), well-defined
  sub-genre tropes — exactly the structural regularity that control codes
  and rhyme-aware fine-tunes thrive on.

---

## 4. State of the field in May 2026

**English lyrics.** Mature open community (Lyre-LM, several Llama-2
fine-tunes). Commercial scene dominated by Suno/Udio integrating lyric and
audio generation end-to-end. Latest research has moved past pure text —
papers like JAM and SegTune are about *lyric-to-song* with vocal control.

**Other-language poetry/lyrics.** Active small communities: Czech (GPT
Czech Poet), Arabic (InstructPoet-AR), French rap (megasliger dataset),
Chinese (mt5 lyrics models). All use roughly the same recipe: continued-pretrain
language base → SFT on lyrics with control codes → some flavor of
rhyme/syllable handling.

**Portuguese.** The base-LM problem is mostly solved (Tucano, Sabiá, Bode,
Albertina ecosystem). The lyric-specific problem is essentially **unsolved
openly**. The infrastructure exists; nobody has done the work.

---

## 5. Implications for this project

Concrete leverage points implied by the survey above:

- **v0 baseline = SFT + control codes** (the simplest of approaches B+C).
  That's already what the [ROADMAP](../ROADMAP.md) says. Don't over-engineer.
- **The biggest single quality lever for sertanejo** will likely be
  Pasini's prepend-rhyme trick (Phase 6 controllability), because sertanejo
  is AABB-heavy. Plan to try this in v1.
- **Syllable-aware tokenization** is intriguing for sertanejo's
  redondilha-maior pattern, but expensive — defer until v2 unless v1 shows
  meter is the dominant failure mode.
- **Forget benchmarks.** Build our own metric stack early (Phase 5) and
  version it. Use it consistently across all checkpoints so we can see
  progress *relative to ourselves*; cross-paper comparison is not on offer.
- **Memorization is a real risk** even at personal scope. Keep aggressive
  dedup and a verbatim-regurgitation check in the eval stack.
- **Don't underestimate Phase 1.** The legal / data-acquisition piece is
  harder than the modeling piece in this domain. Vagalume API + 4MuLA Tiny
  is the cleanest path; avoid scraping letras.mus.br for v0 if possible.
