# SmartSeal — launch & marketing plan (v3.0.0)

*Authentic amplification only: real accounts, real value, disclosed. No sockpuppets,
vote-rings, or fake urgency — for a trust product, one caught manipulation taints the
whole family.*

## Positioning
- **Hook:** "Was this made by a human, an AI, or tampered with after?"
- **One-liner:** Seal what you ship. A signed receipt so anyone can verify what they received.
- **Wedge:** the 10-second `--demo` result people screenshot and pass on.
- **Proof it's real:** ships runnable with a synthetic demo; no signup.

## Channels (one angle each — never cross-post identical copy)

**Hacker News — Show HN.** Lead with the question, not the product. See the ready
draft below.

**Reddit** (r/programming, r/devops, plus the audience sub for this gap): share the
`--demo` as a genuinely useful self-check; let the output do the talking.

**Dev.to / Hashnode:** a data-story — "what I found running SmartSeal across N real
repos/prompts/answers" — tool as the byproduct. Durable SEO tail.

**MCP registry + awesome-lists:** list `sf-smartseal-mcp`; PR into awesome-mcp and the
relevant awesome-devsecops / awesome-ai list.

**X / Bluesky / Mastodon:** the screenshot + the one-liner people can run immediately.

**Newsletters / community Slacks & Discords:** offer the demo as a free useful thing.

## Cross-promotion (the circular, natural stack)
Every launch references the family without feeling like an ad:
- The README's "Part of the Smart* family" table links SmartPangolin, SmartPrompt, SmartCheck, SmartStandard, and back to
  **IAIso** (https://iaiso.org) and **SmartTasks.cloud** (https://smarttasks.cloud).
- The Show HN closes with: "it's one of the Smart* tools implementing the open **IAIso
  §3 · Provenance** standard — the others cover the rest of the AI-adoption gaps."
- Time launches so each tool's post can point at the previous one's traction.

## Enterprise & contact
- Route company/enterprise interest to **[enterprise@smarttasks.cloud](mailto:enterprise@smarttasks.cloud)** —
  "we help teams integrate SmartSeal + IAIso, audit-ready."
- Founder credibility (link where a buyer/journalist would look): Roen Branham (https://www.linkedin.com/in/roen-branham-167ab29/), Le Vu Tanh (https://www.linkedin.com/in/lee-thanh-76aa8ba0/).

## Launch sequencing
1. **T-7d:** repo public, MCP listed, `--demo` polished, IAIso starter-kit links live.
2. **T-1d:** pre-write the Show HN + the data-story; line up your real network for an
   honest first hour.
3. **T-0 (Tue–Thu ~15:00 UTC):** Show HN + the X thread same hour; reply fast.
4. **T+1–2d:** Reddit + newsletter drops while warm.
5. **T+2–4d:** publish the data-story for the quotable tail.
6. **T+1–2wk:** PR into awesome-lists; follow-up post with adoption numbers → restart.

---

## Ready-to-post: Show HN

> **Title:** Show HN: SmartSeal – seal what you ship
>
> Was this made by a human, an AI, or tampered with after? As AI takes over the producing, you consume mixed human/ai artifacts and can't prove or trust their origin. I built SmartSeal to
> `seal` at exactly that moment — deterministic, dependency-free, and it works
> the second you clone it (a synthetic demo is bundled, so you can try it on sample
> data before pointing it at your own).
>
> It's part of a small family of tools (Smart\*) that each close one gap AI's role-change
> opens, all implementing an open standard we're building called IAIso (§3 · Provenance
> here). It's free and Apache-2.0. Repo + one-liner install in the README.
>
> Honest about limits: it's deterministic pattern-matching, not magic — it's a strong
> last line of defense, not a guarantee. Feedback very welcome, especially on the rule set.

## Ready-to-outline: companion article (Dev.to / your blog)
- **Title:** "Was this made by a human, an AI, or tampered with after?"
- **Hook:** the concrete failure story (a real SEAL-class miss).
- **The shift:** why this gap only exists now that AI does the producing.
- **The data:** what running SmartSeal across a real corpus surfaced (charts).
- **The fix in 10s:** the `--demo`, then pointing it at your own work.
- **The bigger picture:** the IAIso standard + the rest of the Smart* family.
- **CTA:** star the repo, adopt IAIso §3 · Provenance, try SmartTasks.cloud.
  Companies wanting hands-on integration: **enterprise@smarttasks.cloud**.

<!-- SMARTTASKS-MODELS:START -->
## Governed local models (SmartTasks on Hugging Face)

Each artifact carries a **SHA-256** so you can prove the weights you run match what was tested — content-addressed provenance, like SmartSeal.

This tool is local-first, so pair it with models you can actually vet. **SmartTasks** publishes 21+ governance-validated GGUF builds on Hugging Face — each with a machine-readable **scorecard** (capability tiers L1 Layman → L5 Agentic, IAIso conformance invariants (pass/warn/fail), OWASP-mapped garak red-team, transparency probes (viewpoint-alignment / over-refusal), and per-file SHA-256). Gate model selection on evidence, not vibes — and every finding, including warnings, is published in full.

→ **[SmartTasks on Hugging Face](https://huggingface.co/smarttasks)** · [Qwen3.6-27B](https://huggingface.co/smarttasks/Qwen3.6-27B-GGUF) (L5 agentic) · [react-agent-coder-llama-3.1-8b](https://huggingface.co/smarttasks/react-agent-coder-llama-3.1-8b-GGUF) (agentic coder) · [gpt-oss-20b](https://huggingface.co/smarttasks/gpt-oss-20b-GGUF) (open reasoning)

| model | size | task |
|---|---|---|
| [Qwen3.6-27B-GGUF](https://huggingface.co/smarttasks/Qwen3.6-27B-GGUF) | 27B | Text Generation |
| [react-agent-coder-llama-3.1-8b-GGUF](https://huggingface.co/smarttasks/react-agent-coder-llama-3.1-8b-GGUF) | 8B | Text Generation |
| [react-agent-coder-gemma-4-e4b-GGUF](https://huggingface.co/smarttasks/react-agent-coder-gemma-4-e4b-GGUF) | 8B | Text Generation |
| [Yi-Coder-9B-Chat-GGUF](https://huggingface.co/smarttasks/Yi-Coder-9B-Chat-GGUF) | 9B | Text Generation |
| [VibeThinker-1.5B-GGUF](https://huggingface.co/smarttasks/VibeThinker-1.5B-GGUF) | 2B | Text Generation |
| [gemma-4-12b-it-GGUF](https://huggingface.co/smarttasks/gemma-4-12b-it-GGUF) | 12B | Text Generation |
| [SmolLM3-3B-GGUF](https://huggingface.co/smarttasks/SmolLM3-3B-GGUF) | 3B | Text Generation |
| [Mistral-Small-3.2-24B-Instruct-GGUF](https://huggingface.co/smarttasks/Mistral-Small-3.2-24B-Instruct-GGUF) | 24B | Text Generation |

… and more at **[huggingface.co/smarttasks](https://huggingface.co/smarttasks)**.
<!-- SMARTTASKS-MODELS:END -->
