# References — pt-BR Lyrics LLM

A curated index of working, leverageable resources for fine-tuning an LLM that
writes Brazilian-Portuguese song lyrics. Links marked **(unverified)** were
surfaced via search but not fetched; confirm before relying on them.

> **Scope.** Base models, datasets, scrapers, papers, fine-tuning frameworks,
> tokenizer guidance, evaluation tooling, communities, hardware/cost references,
> deployment options. Last refreshed: 2026-05-22.

---

## 1. Brazilian Portuguese base / foundation LLMs

Decoder-only / generative models suited for fine-tuning.

| Model | Size | Notes |
|---|---|---|
| [TucanoBR/Tucano-160m](https://huggingface.co/TucanoBR/Tucano-160m) | 160M | Llama arch, natively pretrained on GigaVerbo (200B pt tokens). Apache-2.0. Cheap to iterate on. |
| [TucanoBR/Tucano-630m](https://huggingface.co/TucanoBR/Tucano-630m) | 630M | Same family, mid-tier. |
| [TucanoBR/Tucano-1b1](https://huggingface.co/TucanoBR/Tucano-1b1) | 1.1B | Sweet spot on a single 16-24GB GPU. |
| [TucanoBR/Tucano-1b1-Instruct](https://huggingface.co/TucanoBR/Tucano-1b1-Instruct) | 1.1B | Instruction-tuned (uses [Tucano-SFT](https://huggingface.co/datasets/TucanoBR/Tucano-SFT)). |
| [TucanoBR/Tucano-2b4](https://huggingface.co/TucanoBR/Tucano-2b4) | 2.4B | Largest base in the open Tucano family. |
| [TucanoBR/Tucano-2b4-Instruct](https://huggingface.co/TucanoBR/Tucano-2b4-Instruct) | 2.4B | Instruction-tuned. **Recommended starting point.** |
| [cnmoro/Tucano-160m-Portuguese-Instruct-v2](https://huggingface.co/cnmoro/Tucano-160m-Portuguese-Instruct-v2) | 160M | Community SFT on multiple pt instruct datasets. Apache-2.0. |
| [maritaca-ai/sabia-7b](https://huggingface.co/maritaca-ai/sabia-7b) | 7B | Llama-1 continued-pretrain on 10B pt tokens (ClueWeb22). **LLaMA-1 research-only license**, no commercial use. |
| [TheBloke/sabia-7B-GGUF](https://huggingface.co/TheBloke/sabia-7B-GGUF), [lucianosb/sabia-7b-GGUF](https://huggingface.co/lucianosb/sabia-7b-GGUF) | 7B (Q*) | Quantized Sabiá for llama.cpp/Ollama. Same license caveat. |
| [recogna-nlp/bode-7b-alpaca-pt-br](https://huggingface.co/recogna-nlp/bode-7b-alpaca-pt-br) | 7B | Llama-2 + pt-Alpaca SFT. Llama-2 community license. |
| [recogna-nlp/bode-13b-alpaca-pt-br](https://huggingface.co/recogna-nlp/bode-13b-alpaca-pt-br) | 13B | Largest open pt-instruct model in this family. |
| [recogna-nlp/Phi-Bode](https://huggingface.co/recogna-nlp/Phi-Bode) | 2.7B | Phi-2 + pt-Alpaca; lighter VRAM. |
| [recogna-nlp (org)](https://huggingface.co/recogna-nlp) | — | Hosts the full Bode family, Mistral-Bode, GGUF builds. |
| [NOVA-vision-language/GlorIA-1.3B](https://huggingface.co/NOVA-vision-language/GlorIA-1.3B) | 1.3B | GPT-Neo trained on 35B pt tokens — **pt-PT focused**, expect Portuguese-from-Portugal bias. Paper: [arXiv 2402.12969](https://arxiv.org/abs/2402.12969). |
| [pierreguillou/gpt2-small-portuguese](https://huggingface.co/pierreguillou/gpt2-small-portuguese) | 124M | Older GPT-2 small pt fine-tune; cheap toy baseline. |
| [rsmonteiro/gpt2-small-portuguese-lyrics](https://huggingface.co/rsmonteiro/gpt2-small-portuguese-lyrics) | 124M | **Direct prior art**: GPT-2 small fine-tuned on pt-BR lyrics. MIT license. |
| [PORTULAN/gervasio-8b-portuguese-ptbr-decoder](https://huggingface.co/PORTULAN/gervasio-8b-portuguese-ptbr-decoder) (unverified) | 8B | Llama-3 8B decoder adapted to pt-BR. Check license per model card. |

**Encoder-only** (useful for classification, NER, retrieval, BERTScore — **not** for generation):

- [neuralmind/bert-base-portuguese-cased](https://huggingface.co/neuralmind/bert-base-portuguese-cased) — BERTimbau base. Apache-2.0.
- [neuralmind/bert-large-portuguese-cased](https://huggingface.co/neuralmind/bert-large-portuguese-cased) — BERTimbau large.
- [PORTULAN/albertina-900m-portuguese-ptbr-encoder-brwac](https://huggingface.co/PORTULAN/albertina-900m-portuguese-ptbr-encoder-brwac) — 900M DeBERTa encoder, research license.
- [PORTULAN/albertina-1b5-portuguese-ptbr-encoder](https://huggingface.co/PORTULAN/albertina-1b5-portuguese-ptbr-encoder) — 1.5B variant.
- DeBERTinha — paper [arXiv 2309.16844](https://arxiv.org/abs/2309.16844); 40M params, very efficient.
- [Open Portuguese LLM Leaderboard best models](https://huggingface.co/collections/eduagarcia/portuguese-llm-leaderboard-best-models) — community ranking, updated regularly.

**Tradeoffs.** Tucano is the most open and pt-native; Sabiá-7B has the best raw pt quality at 7B but is research-only; Bode-13B is the largest accessible instruction-tuned pt model. For production, also consider fine-tuning a multilingual base (Mistral-7B, Llama-3-8B, Qwen2.5-7B) directly — they already have decent pt-BR coverage and permissive licenses.

---

## 2. Lyrics datasets

### Lyrics — pt-BR or multilingual

- [4MuLA (GitHub)](https://github.com/4mulaDataset/4mula) — 96,458 songs / 15,310 artists / 76 genres, scraped from Vagalume; lyrics + audio features. Research-only.
- [4MuLA ACM paper](https://dl.acm.org/doi/10.1145/3428658.3431089) and [4MuLA Tiny on Zenodo](https://zenodo.org/records/4585498) — citable + downloadable subsets.
- [English-Portuguese parallel lyrics corpus (Martins 2020)](https://opencor.gitlab.io/corpora/martins20parallel/) **(unverified)** — 936 artists, ~1.93M pt sentences, ~23k aligned pt-en pairs from letras.mus.br.
- [sheacon/song_lyrics](https://huggingface.co/datasets/sheacon/song_lyrics) — ~3.3M multilingual lyrics with metadata; English-heavy but contains pt.
- [Retrato Cantado (PROPOR 2026)](https://aclanthology.org/2026.propor-1.68/) — annotated Brazilian song lyrics for predicative constructions; small but linguistically rich.

### Lyrics — non-pt (useful for transfer learning of "lyric form")

- [amishshah/song_lyrics](https://huggingface.co/datasets/amishshah/song_lyrics) — 1M+ rows, English; permissive at the dataset level (lyric copyright still applies upstream).
- [sebastiandizon/genius-song-lyrics](https://huggingface.co/datasets/sebastiandizon/genius-song-lyrics) — ~5M Genius lyrics.
- [anantg/genius-song-lyrics](https://huggingface.co/datasets/anantg/genius-song-lyrics) — Parquet snapshot of Genius.
- [aifeifei798/song_lyrics_min](https://huggingface.co/datasets/aifeifei798/song_lyrics_min) — Cleaned subset of `amishshah/song_lyrics`. Apache-2.0.
- [ThatOneShortGuy/SongLyrics](https://huggingface.co/datasets/ThatOneShortGuy/SongLyrics) — Lyrics + cover art + popularity. OpenRail++.
- [SpartanCinder/song-lyrics-artist-classifier](https://huggingface.co/datasets/SpartanCinder/song-lyrics-artist-classifier) — Lyrics by artist; CC-BY-NC-SA-4.0.
- [juliensimon/autonlp-data-song-lyrics](https://huggingface.co/datasets/juliensimon/autonlp-data-song-lyrics) — 53,882 English lyrics labeled by 6 genres; good for genre-conditioning experiments.
- [metncelik/turkish-song-lyrics](https://huggingface.co/datasets/metncelik/turkish-song-lyrics) — Template for the "small-language lyrics" problem we face.
- [megasliger/french_rap_lyrics_completion_generation_theme_lyrics_081224](https://huggingface.co/datasets/megasliger/french_rap_lyrics_completion_generation_theme_lyrics_081224) — example schema for theme-conditioned completion.
- [WASABI Song Corpus](https://arxiv.org/abs/1912.02477) — 1.73M songs (1.41M unique lyrics) with structure/topic/emotion annotations. Strong reference for *annotated* lyrics datasets.
- [Song Lyrics Dataset (Kaggle, deepshah16)](https://www.kaggle.com/datasets/deepshah16/song-lyrics-dataset) — general English lyrics dataset.

### General pt-BR corpora (for continued pretraining / vocab work)

- [bastao/VeraCruz_PT-BR](https://huggingface.co/datasets/bastao/VeraCruz_PT-BR) — ~190M samples of pt content, split PT vs BR by URL metadata.
- [carolina-c4ai/corpus-carolina](https://huggingface.co/datasets/carolina-c4ai/corpus-carolina) — Carolina corpus with provenance + typology metadata. Paper: [arXiv 2303.16098](https://arxiv.org/abs/2303.16098).
- [UFRGS/brwac](https://huggingface.co/datasets/UFRGS/brwac) — 2.7B-token Brazilian web corpus; restrictive license.
- [oscar-corpus/OSCAR-2301](https://huggingface.co/datasets/oscar-corpus/OSCAR-2301) — multilingual Common Crawl, with pt subset.
- [TucanoBR/Tucano-SFT](https://huggingface.co/datasets/TucanoBR/Tucano-SFT) — Instruction-tuning data used for Tucano-Instruct.
- [adalbertojunior/openHermes_portuguese](https://huggingface.co/datasets/adalbertojunior/openHermes_portuguese) — translated OpenHermes for pt SFT.
- [cnmoro/smoltalk-555k-ptbr](https://huggingface.co/datasets/cnmoro/smoltalk-555k-ptbr) — 555k pt-BR conversational examples.
- [Brazilian Portuguese Datasets collection](https://huggingface.co/collections/ai-eldorado/brazilian-portuguese-datasets) — community-curated index.

**Licensing reality check.** Brazilian song lyrics are administered by ECAD. 4MuLA and any letras.mus.br/Vagalume scrape are distributed for research; commercial deployment of a model trained on them is legally risky. There is **no settled fair-use precedent in Brazil** for AI training. Document provenance for every track.

---

## 3. Lyrics scraping / collection tools

### Vagalume

- [Vagalume API docs](https://api.vagalume.com.br/docs/letras/) — Official API, free with rate limits, key required. ToS allows non-commercial use with attribution.
- [paladini/vagalume-download-lyrics](https://github.com/paladini/vagalume-download-lyrics) — Download all of an artist's lyrics.
- [diegoaltx/python-vagalume](https://github.com/diegoaltx/python-vagalume) — Python wrapper for the Vagalume API.
- [pedrohbtp/vagalume-python3](https://github.com/pedrohbtp/vagalume-python3) — Alternative Python 3 client.

### letras.mus.br

- [Fernando-Erd/letras-scraper](https://github.com/Fernando-Erd/letras-scraper) — Composer + genre extraction.
- [datalivre/web-scraping](https://github.com/datalivre/web-scraping) — Artist/band scraper (pt README).
- [celsocelante/lyrics-grabber](https://github.com/celsocelante/lyrics-grabber) — Vagalume + letras.mus.br, JSON output.

### Genius

- [lyricsgenius (PyPI)](https://pypi.org/project/lyricsgenius/) · [docs](https://lyricsgenius.readthedocs.io/en/master/) — Standard Genius client.
- [elliebirbeck/genius-lyrics-scraper](https://github.com/elliebirbeck/genius-lyrics-scraper) — Minimal bulk-scrape example.
- [Scraping Genius lyrics (John W. Millr)](https://www.johnwmillr.com/scraping-genius-lyrics/) — Reference tutorial.

### Multi-source

- [AmanoTeam/LyricsPy](https://github.com/AmanoTeam/LyricsPy) — Unified Musixmatch + Genius + letras.mus.br client.

**Legal note.** `letras.mus.br` ToS prohibits scraping for redistribution. Vagalume's API explicitly allows non-commercial use with attribution. Genius officially exposes metadata only; the lyric text comes from HTML scraping (grey area). For production, license through **Musixmatch** or **LyricFind**.

---

## 4. Academic papers

### pt / Brazilian-Portuguese LLMs and corpora

- [Sabiá: Portuguese Large Language Models — arXiv 2304.07880](https://arxiv.org/abs/2304.07880) — Original Sabiá.
- [Sabiá-3 Technical Report — arXiv 2410.12049](https://arxiv.org/abs/2410.12049) — Latest Maritaca flagship.
- [Tucano: Advancing Neural Text Generation for Portuguese — arXiv 2411.07854](https://arxiv.org/abs/2411.07854) — End-to-end open recipe (GigaVerbo corpus + Tucano models).
- [GlórIA: A Generative and Open Large Language Model for Portuguese — arXiv 2402.12969](https://arxiv.org/abs/2402.12969) — pt-PT focused; introduces CALAME-PT.
- [Carolina: General Corpus of Contemporary Brazilian Portuguese — arXiv 2303.16098](https://arxiv.org/abs/2303.16098).
- [PTT5: Pretraining T5 on Brazilian Portuguese — arXiv 2008.09144](https://arxiv.org/abs/2008.09144) — Older but practical with public code.
- [DeBERTinha: Adapting DebertaV3 for pt-BR — arXiv 2309.16844](https://arxiv.org/abs/2309.16844) — Concrete vocab-expansion + continued-pretraining recipe.
- [Albertina PT* family — arXiv 2403.01897](https://arxiv.org/abs/2403.01897) — pt encoder ecosystem.
- [PORTULAN ExtraGLUE — arXiv 2404.05333](https://arxiv.org/abs/2404.05333) — pt benchmark + LoRA fine-tunes.
- [PeLLE: Encoder-based LMs for Brazilian Portuguese — arXiv 2402.19204](https://arxiv.org/abs/2402.19204).
- [BRoverbs: Measuring how much LLMs understand Portuguese proverbs — arXiv 2509.08960](https://arxiv.org/abs/2509.08960) — Cultural-knowledge benchmark.
- [Automatic generation of creative text in Portuguese: an overview](https://link.springer.com/article/10.1007/s10579-023-09646-3) · [PMC mirror](https://pmc.ncbi.nlm.nih.gov/articles/PMC10155647/) — **The most directly relevant single paper for this project** (covers PoeTryMe, Tra-la-Lyrics, GPT-2 pt poetry).
- [Open-source rule-based syllabification tool for pt-BR (J. Braz. Comp. Soc.)](https://journal-bcs.springeropen.com/articles/10.1186/s13173-014-0021-9).
- [Implementation of an Automatic Syllabic Division Algorithm for Portuguese — arXiv 1501.07496](https://arxiv.org/abs/1501.07496).

### Lyrics, poetry, and controllable generation

- [Encoder-Decoder Framework for Free Verses with Controllable Rhyming — arXiv 2405.05176](https://arxiv.org/abs/2405.05176) — Prepend-the-rhyme-word fine-tune; multilingual.
- [Song Form-aware Full-Song Text-to-Lyrics Generation with Multi-Level Granularity Syllable Count Control — arXiv 2411.13100](https://arxiv.org/abs/2411.13100).
- [GPT Czech Poet — arXiv 2407.12790](https://arxiv.org/abs/2407.12790) — Syllable-level tokenization + forced generation for poetic strophes; very transferable to pt.
- [DeepRapper: Neural Rap Generation with Rhyme and Rhythm Modeling — arXiv 2107.01875](https://arxiv.org/abs/2107.01875) · [project page](https://ai-muzic.github.io/deeprapper/) — Standard reference for rhyme+rhythm-aware lyric LMs.
- [PoeLM: Meter- and Rhyme-Controllable LM for Unsupervised Poetry Generation — arXiv 2205.12206](https://arxiv.org/abs/2205.12206) — Control-code approach.
- [SongRewriter — arXiv 2211.15037](https://arxiv.org/abs/2211.15037) — Controllable rewriting under existing melody.
- [Raply: profanity-mitigated rap generator — arXiv 2407.06941](https://arxiv.org/abs/2407.06941).
- [DopeLearning: Computational Rap Generation — arXiv 1505.04771](https://arxiv.org/abs/1505.04771) — Classic baseline.
- [Weird AI Yankovic: Generating Parody Lyrics — arXiv 2009.12240](https://arxiv.org/abs/2009.12240).
- [WASABI Song Corpus — arXiv 1912.02477](https://arxiv.org/abs/1912.02477).
- [Melody-Lyrics Matching with Contrastive Alignment — arXiv 2508.00123](https://arxiv.org/abs/2508.00123).
- [Controllable Text Generation for LLMs: A Survey — arXiv 2408.12599](https://arxiv.org/abs/2408.12599).
- [Toward Unified Controllable Text Generation via Regular Expression Instruction — arXiv 2309.10447](https://arxiv.org/abs/2309.10447).
- [Instruction-Guided Poetry Generation in Arabic and Its Dialects](https://github.com/mbzuai-nlp/instructpoet-ar) — Recipe for instruction-tuned, form-aware poetry in a non-English language.

---

## 5. Fine-tuning frameworks & tutorials

### Core frameworks

- [Unsloth fine-tuning guide](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide) — **Fastest path on a single consumer GPU** (4-bit QLoRA, Llama/Mistral/Qwen/Gemma). Recommended.
- [Axolotl docs](https://docs.axolotl.ai/) — Config-file-driven training; integrates Unsloth kernels.
- [LLaMA-Factory SFT docs](https://llamafactory.readthedocs.io/en/latest/getting_started/sft.html) — GUI + CLI; many presets.
- [Hugging Face TRL — SFTTrainer](https://huggingface.co/docs/trl/sft_trainer) — Canonical SFT entrypoint (packing, completion-only loss, LoRA/QLoRA).
- [HF PEFT — LoRA task guides](https://huggingface.co/docs/peft/en/task_guides/lora_based_methods).
- [Philipp Schmid: Fine-tune Llama-3 with FSDP + QLoRA](https://www.philschmid.de/fsdp-qlora-llama3) — Multi-GPU recipe.
- [Neptune: Fine-Tuning Llama-3 with LoRA](https://neptune.ai/blog/fine-tuning-llama-3-with-lora) — Current end-to-end article.

### Lyrics-specific prior art

- [Christianfoley/LLMLyricGen (Lyre-LM)](https://github.com/Christianfoley/LLMLyricGen) — Llama-2-7B fine-tune for English lyric generation. **Closest pipeline to copy and adapt.**
- [ewenme/gpt-2-raps](https://github.com/ewenme/gpt-2-raps) — Minimal GPT-2 rap fine-tune.
- [sfs0126/Lyric-Generator-fine-tuned-GPT-2](https://github.com/sfs0126/Lyric-Generator-fine-tuned-GPT-2) — Genre-conditioned GPT-2.
- [Pierre Guillou: fine-tuning English GPT-2 into Portuguese (notebook)](https://github.com/piegu/fastai-projects/blob/master/finetuning-English-GPT2-any-language-Portuguese-HuggingFace-fastaiv2.ipynb) — Classic "fine-tune English LM into pt" walkthrough.

---

## 6. Tokenizer / vocabulary for pt-BR

- ["How Can We Effectively Expand the Vocabulary of LLMs with 0.01GB of Target Language Text?" — arXiv 2406.11477](https://arxiv.org/abs/2406.11477) — Low-resource vocab expansion; directly relevant.
- [Vocabulary Customization for Domain-Specific LLM Deployment — arXiv 2509.26124](https://arxiv.org/abs/2509.26124) — Treat lyrics as the "domain."
- [Vocabulary Replacement in SentencePiece (PACLIC 2023)](https://aclanthology.org/2023.paclic-1.64.pdf).
- [DeBERTinha — arXiv 2309.16844](https://arxiv.org/abs/2309.16844) — Concrete pt-BR vocab adaptation recipe.
- [HF tokenizers library](https://huggingface.co/docs/tokenizers/index) — Train BPE/Unigram tokenizers.
- [Kimamani NLP: vocabulary expansion for BPE](https://gucci-j.github.io/post/en/vocab-expansion/) — Practical walkthrough.
- [SentencePiece](https://github.com/google/sentencepiece) — Reference tokenizer.

**Practical note.** Many multilingual base models over-fragment pt-BR words ("saudade", "coração", common contractions "pra"/"tá"). Tucano avoids this since it was trained from scratch with a pt vocabulary; if you start from Llama/Mistral, budget time for vocab extension. The DeBERTinha and Tucano papers describe the recipe.

---

## 7. Evaluation methods for lyrics / poetry

### Syllable & rhyme tools (pt-BR)

- [evelinamorim/syllable-pt](https://github.com/evelinamorim/syllable-pt) — Rule-based pt-BR syllable splitter.
- [centraldedados/linguistica-silabas](https://github.com/centraldedados/linguistica-silabas) — pt syllable data + lib.
- [silabeador (PyPI)](https://pypi.org/project/silabeador/) — Spanish/Portuguese syllable counter.
- [Pyphen](https://pyphen.org/) — Hyphenation with pt-BR dictionary; ~15% segmentation error rate — ensemble with rule-based libs.
- [Fonology (Guilherme D. Garcia)](https://gdgarcia.ca/fonology.html) — pt phonology toolkit (stress / weight analysis) used in academic studies.
- [prosodic (PyPI)](https://pypi.org/project/prosodic/) — Phoneme & rhyme analysis; English/Finnish out of the box, adaptable.
- [Open-source rule-based syllabification tool for pt-BR](https://journal-bcs.springeropen.com/articles/10.1186/s13173-014-0021-9) — Algorithm spec (claims 99% accuracy) for reimplementation.

### General NLP eval (use pt models as backbone)

- [BERTScore — arXiv 1904.09675](https://arxiv.org/abs/1904.09675) — Pair with BERTimbau as the scoring model for pt-BR.
- [HF evaluate](https://huggingface.co/docs/evaluate/index) — BLEU/ROUGE/BERTScore/perplexity wrappers.
- [Stanza pipeline](https://stanfordnlp.github.io/stanza/) — Tokenization/POS/lemma for pt.
- [spaCy pt models](https://spacy.io/models/pt) — `pt_core_news_lg` for NER/parsing.
- [Open Portuguese LLM Leaderboard](https://huggingface.co/spaces/eduagarcia/open_pt_llm_leaderboard) — Tasks: ENEM, BLUEX, ASSIN2, FAQUAD. Use as a "general pt fluency" sanity check.
- [eduagarcia/lm-evaluation-harness-pt](https://github.com/eduagarcia/lm-evaluation-harness-pt) — Harness for the leaderboard.

**Recommended evaluation stack for this project.**

1. Perplexity on a held-out lyrics test set.
2. Per-line syllable-count compliance (syllable-pt + Pyphen ensemble).
3. End-rhyme accuracy via pt phonetic last-syllable matching.
4. BERTScore vs. reference lyrics, backbone = BERTimbau.
5. ~50-sample human evaluation by Brazilian speakers on grammaticality, poeticness, and genre fit.

---

## 8. Communities & discussion

- [Brasileiras em PLN](https://brasileiraspln.com/) — 200+ Brazilian women NLP practitioners; community, blog, open-access didactic book.
- [ajdavidl/Portuguese-NLP (awesome list)](https://github.com/ajdavidl/Portuguese-NLP) — **Single best community-maintained index** of pt NLP tools, datasets, models.
- [Maritaca AI](https://www.maritaca.ai/en/) · [Maritaca on X](https://x.com/maritacaai) — Industrial pt-LLM team.
- [Open Portuguese LLM Leaderboard discussions](https://huggingface.co/spaces/eduagarcia/open_pt_llm_leaderboard/discussions) — Most active venue for new pt-LLM releases.
- [Hugging Face Forums](https://discuss.huggingface.co/) — Search for `portuguese`, `tokenizer pt`, `lyrics`. Notable thread: [PreTrain RoBERTa from scratch in Portuguese](https://discuss.huggingface.co/t/pretrain-roberta-from-scratch-in-portuguese/7272).
- [r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/) — Search `Portuguese`, `Sabia`, `Tucano`, `Bode`.
- [PROPOR (Conf. on Computational Processing of Portuguese)](https://propor.di.uevora.pt/) **(unverified URL — drifts per year)** — Main pt-NLP venue.
- NILC (Núcleo Interinstitucional de Linguística Computacional, USP) — Brazil's leading academic pt-NLP lab; many tools/datasets trace back here.

---

## 9. Hardware / cost guides

- [Runpod LLM fine-tuning GPU guide](https://www.runpod.io/blog/llm-fine-tuning-gpu-guide) — VRAM per model size / quantization.
- [Runpod LoRA/QLoRA on a budget](https://www.runpod.io/articles/guides/how-to-fine-tune-large-language-models-on-a-budget).
- [Runpod pricing](https://www.runpod.io/pricing).
- [computeprices: RunPod vs Vast.ai 2026](https://computeprices.com/compare/runpod-vs-vast).
- [Fine-Tune LLMs for Under $20 (Medium)](https://medium.com/@velinxs/how-to-fine-tune-llms-for-under-20-step-by-step-c187a3059ca2).
- [Fine-Tune Mistral-7B on Colab (Medium)](https://medium.com/@charlesduyilemi/fine-tune-mistral-7b-like-a-pro-complete-guide-with-colab-12c4240b3831).
- [QLoRA Fine-Tuning: Train 70B on 24GB GPU](https://localaimaster.com/blog/qlora-fine-tuning-guide).
- Google Colab free tier (T4 16GB) and Kaggle (2× T4 16GB, ~30h/week free) — both viable for ≤7B QLoRA.

**Realistic numbers.** 7B QLoRA fits in ~8-12GB VRAM (free Colab T4 is borderline; Kaggle 2×T4 comfortable). One SFT pass over ~50k lyric examples for 2-3 epochs runs in ~2-4h on a single A100 (~$5-15 on RunPod/Vast.ai). Budget another $5-10 for evaluation/inference exploration.

---

## 10. Inference & local deployment

- [llama.cpp](https://github.com/ggml-org/llama.cpp) — Reference CPU+GPU engine; origin of the GGUF format.
- [Ollama](https://ollama.com/) — Single-binary local LLM server with OpenAI-compatible API; easiest demo path.
- [vLLM](https://github.com/vllm-project/vllm) — High-throughput GPU serving; pick this for many concurrent users.
- [text-generation-webui (oobabooga)](https://github.com/oobabooga/text-generation-webui) — Browser UI over multiple backends.
- [HF docs: GGUF on the Hub](https://huggingface.co/docs/hub/gguf-llamacpp).
- [Red Hat: vLLM vs llama.cpp comparison](https://developers.redhat.com/articles/2025/09/30/vllm-or-llamacpp-choosing-right-llm-inference-engine-your-use-case).

**Ready-quantized pt models for direct use / comparison:**

- [TheBloke/sabia-7B-GGUF](https://huggingface.co/TheBloke/sabia-7B-GGUF), [TheBloke/sabia-7B-AWQ](https://huggingface.co/TheBloke/sabia-7B-AWQ).
- [tensorblock/Tucano-2b4-Instruct-GGUF](https://huggingface.co/tensorblock/Tucano-2b4-Instruct-GGUF).
- [mradermacher/Tucano-160m-Portuguese-Instruct-v2-GGUF](https://huggingface.co/mradermacher/Tucano-160m-Portuguese-Instruct-v2-GGUF).
- [cnmoro/Tucano-160m-Portuguese-Instruct-ONNX](https://huggingface.co/cnmoro/Tucano-160m-Portuguese-Instruct-ONNX).
- [recogna-nlp/bode-7b-alpaca-pt-br-gguf](https://huggingface.co/recogna-nlp/bode-7b-alpaca-pt-br-gguf), [bode-13b-alpaca-pt-br-gguf](https://huggingface.co/recogna-nlp/bode-13b-alpaca-pt-br-gguf).

**Recommended path.** LoRA fine-tune in BF16 → merge adapters → convert with `llama.cpp/convert_hf_to_gguf.py` → quantize to Q4_K_M or Q5_K_M → serve via Ollama (or vLLM for higher throughput).

---

## 11. Notable gaps & risks

- **Copyright.** Brazilian song lyrics are protected by ECAD-administered rights. Training on scraped Vagalume / letras.mus.br / Genius data is research-territory only. No settled fair-use precedent in Brazil for AI training (see [Beyond English: Multilingual Bias in LLM Copyright Compliance — arXiv 2503.05713](https://arxiv.org/abs/2503.05713)). Commercial use likely needs licensed data via Musixmatch or LyricFind.
- **Data sparsity.** No large, openly licensed pt-BR lyrics dataset exists; 4MuLA (~96k songs) is research-only. Expect to build a curated dataset, which inherits the copyright risk.
- **Tokenizer drift.** Most multilingual base models fragment pt orthography (diacritics, "pra"/"tá") which hurts quality and inference cost. Tucano avoids this; with Llama/Mistral base, budget for vocab extension.
- **Evaluation maturity.** No established benchmark for pt-BR lyric generation. Roll your own metric stack (syllable + rhyme + BERTScore + human eval).
- **Genre coverage.** Datasets skew toward MPB, sertanejo, samba. Funk, trap, gospel, and regional styles (forró, brega, frevo) are under-represented and harder to scrape legally.
- **Community size.** pt-BR LLM community is small. Niche tokenizer/eval questions may go unanswered — Brasileiras em PLN, the eduagarcia leaderboard discussions, and r/LocalLLaMA threads tagged "pt" are the most active venues.
- **Link freshness.** HF orgs occasionally rename/remove models; arXiv IDs are stable. Re-verify model URLs before depending on them.
