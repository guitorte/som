"""Zero-shot lyric generation across candidate base models.

Phase 0 of the lyrics-llm roadmap. Loads a model, runs each prompt from a
JSON file, and writes completions to a JSON results file. Designed to run
on a single free-tier Colab T4 (16GB).

Example:
    python scripts/zero_shot.py \\
        --model TucanoBR/Tucano-630m \\
        --prompts evaluation/prompts/sertanejo_prompts.json \\
        --out docs/00-zero-shot-Tucano-630m.json
"""

from __future__ import annotations

import argparse
import gc
import json
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


DTYPES = {
    "float16": torch.float16,
    "bfloat16": torch.bfloat16,
    "float32": torch.float32,
}


def load_prompts(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        prompts = json.load(f)
    if not isinstance(prompts, list):
        raise ValueError(f"Prompts file {path} must contain a JSON list.")
    return prompts


def load_model(model_id: str, dtype: torch.dtype):
    tok = AutoTokenizer.from_pretrained(model_id)
    if tok.pad_token_id is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=dtype,
        device_map="auto",
    )
    model.eval()
    return tok, model


@torch.no_grad()
def generate(
    tok,
    model,
    prompt: str,
    max_new_tokens: int,
    temperature: float,
    top_p: float,
    repetition_penalty: float,
) -> str:
    inputs = tok(prompt, return_tensors="pt").to(model.device)
    out = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=temperature,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
        pad_token_id=tok.pad_token_id,
    )
    return tok.decode(out[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", required=True, help="HF model ID")
    ap.add_argument("--prompts", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--max-new-tokens", type=int, default=300)
    ap.add_argument("--temperature", type=float, default=0.85)
    ap.add_argument("--top-p", type=float, default=0.9)
    ap.add_argument("--repetition-penalty", type=float, default=1.15)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--dtype", default="float16", choices=list(DTYPES))
    args = ap.parse_args()

    torch.manual_seed(args.seed)

    prompts = load_prompts(args.prompts)
    print(f"Loaded {len(prompts)} prompts from {args.prompts}.")

    tok, model = load_model(args.model, DTYPES[args.dtype])
    n_params = sum(p.numel() for p in model.parameters())
    print(f"Loaded {args.model} ({n_params / 1e6:.1f}M params) on {model.device}.")

    samples = []
    for i, p in enumerate(prompts, 1):
        prompt_text = p["prompt"]
        print(f"  [{i}/{len(prompts)}] {p.get('id', '?')} ({p.get('sub_genre', '?')})")
        completion = generate(
            tok,
            model,
            prompt_text,
            args.max_new_tokens,
            args.temperature,
            args.top_p,
            args.repetition_penalty,
        )
        samples.append(
            {
                "prompt_id": p.get("id"),
                "sub_genre": p.get("sub_genre"),
                "prompt": prompt_text,
                "completion": completion,
            }
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        json.dump(
            {
                "model": args.model,
                "n_params": n_params,
                "params": {
                    "max_new_tokens": args.max_new_tokens,
                    "temperature": args.temperature,
                    "top_p": args.top_p,
                    "repetition_penalty": args.repetition_penalty,
                    "seed": args.seed,
                    "dtype": args.dtype,
                },
                "samples": samples,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )
    print(f"Wrote {args.out}")

    del model, tok
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
