<!-- mcp-name: io.github.smarttasksorg/smartseal · part of the Smart* family -->
<h1 align="center">🦔 SmartSeal</h1>
<p align="center"><b>Seal what you ship. A signed receipt so anyone can verify what they received.</b></p>
<p align="center">
  <a href="https://iaiso.org">IAIso §3 · Provenance</a> ·
  <a href="https://smarttasks.cloud">SmartTasks.cloud</a> ·
  <a href="#part-of-the-smart-family">the Smart* family</a>
</p>

---

## Was this made by a human, an AI, or tampered with after?

As AI reshapes how we work, a new gap opens: you consume mixed human/ai artifacts and can't prove or trust their origin. **SmartSeal** closes it —
`seal` at the exact moment the gap bites, and it works the second you clone it
(a synthetic demo ships in `demo/`).

```bash
pip install smartseal
smartseal --demo        # run against the bundled demo
```

## Run it in your stack

| Where you work | How you run it |
|---|---|
| **Python** | `pip install smartseal` |
| **Go · Java · Node · PHP** | native ports in [`ports/`](ports/), each verified against the Python reference by [`ports/conformance/run.sh`](ports/conformance/run.sh) |
| **CI / pre-commit** | add the hook from [`.pre-commit-hooks.yaml`](.pre-commit-hooks.yaml) |

## What's in this repo

- **Core engine** — [`src/smartseal/`](src/smartseal/): seal() -> Receipt; verify() -> VerifyResult. Deterministic, dependency-free.
- **CLI** — `smartseal --demo` (and `--version`): a deterministic demo of the core.
- **Language ports** — [`ports/`](ports/): native Go, Java, Node, PHP implementations that reproduce the Python reference, with a shared conformance harness.
- **Also included** — a runnable [`demo/`](demo/), [`examples/`](examples/), the IAIso mapping [`spec/iaiso-map.json`](spec/iaiso-map.json), a browser [`site/playground.html`](site/playground.html), plus public smoke tests in `tests/`.

## How it works

Rule IDs are namespaced `SEAL-*` so output looks kin to the rest of the family
(SmartPangolin's `SEC-*`, etc.). Deterministic, dependency-free, fail-loud.

### The data objects (UML)

These are real dataclasses in [`src/smartseal/models.py`](src/smartseal/models.py) — the
diagram and the code are the same thing:

```mermaid
classDiagram
    class Manifest {
      +artifact: str
      +sha256: str
      +created: str
    }
    class Receipt {
      +manifest: Manifest
      +signature: str
      +chain: list[str]
    }
    class VerifyResult {
      +valid: bool
      +tampered: bool
      +chain_len: int
    }
    class IAIsoControl {
      +section: str
      +name: str
    }
    VerifyResult ..> IAIsoControl : conforms to
```

## Where it sits in the architecture

SmartSeal doesn't stand alone — it stacks with the family, and everything conforms to
the IAIso standard — the same standard that governs SmartTasks' own apps, while each tool here stays standalone and drops into your architecture:

```mermaid
graph LR
    IAIso([IAIso standard]):::std
    Cloud([SmartTasks.cloud]):::cloud
    SmartPangolin[SmartPangolin]:::tool
    SmartPrompt[SmartPrompt]:::tool
    SmartCheck[SmartCheck]:::tool
    SmartSeal[SmartSeal]:::tool
    SmartStandard[SmartStandard]:::tool
    SmartSim[SmartSim]:::tool
    SmartMoat[SmartMoat]:::tool
    SmartRoute[SmartRoute]:::tool
    SmartFeed[SmartFeed]:::tool
    SmartPangolin -->|emits clean artifacts to| SmartSeal
    SmartPrompt -->|hands secret/PII flags to| SmartPangolin
    SmartPrompt -->|enforces prompt rules from| SmartStandard
    SmartCheck -->|stamps verified output with| SmartSeal
    SmartCheck -->|checks against rules from| SmartStandard
    SmartSeal -->|issues receipts consumed by| SmartCheck
    SmartSeal -->|issues receipts consumed by| SmartRoute
    SmartStandard -->|supplies rule sets to| SmartPrompt
    SmartStandard -->|supplies rule sets to| SmartCheck
    SmartSim -->|feeds role forecasts to| SmartMoat
    SmartSim -->|draws signals from| SmartFeed
    SmartMoat -->|consumes forecasts from| SmartSim
    SmartRoute -->|verifies receipts from| SmartSeal
    SmartRoute -->|enforces the standard from| SmartStandard
    SmartFeed -->|feeds signals to| SmartSim
    SmartFeed -->|feeds signals to| SmartMoat
    SmartPangolin -.conforms.-> IAIso
    SmartPangolin -.shares IAIso with.-> Cloud
    SmartPrompt -.conforms.-> IAIso
    SmartPrompt -.shares IAIso with.-> Cloud
    SmartCheck -.conforms.-> IAIso
    SmartCheck -.shares IAIso with.-> Cloud
    SmartSeal -.conforms.-> IAIso
    SmartSeal -.shares IAIso with.-> Cloud
    SmartStandard -.conforms.-> IAIso
    SmartStandard -.shares IAIso with.-> Cloud
    SmartSim -.conforms.-> IAIso
    SmartSim -.shares IAIso with.-> Cloud
    SmartMoat -.conforms.-> IAIso
    SmartMoat -.shares IAIso with.-> Cloud
    SmartRoute -.conforms.-> IAIso
    SmartRoute -.shares IAIso with.-> Cloud
    SmartFeed -.conforms.-> IAIso
    SmartFeed -.shares IAIso with.-> Cloud
    IAIso -.governs.-> Cloud
    classDef tool fill:#1c232d,stroke:#f5b83d,color:#efe9f5;
    classDef std fill:#04121f,stroke:#46d6c8,color:#46d6c8;
    classDef cloud fill:#1a1327,stroke:#a78bfa,color:#a78bfa;
    style SmartSeal stroke-width:3px,stroke:#ff6b6b;
```

- **SmartSeal issues receipts consumed by SmartCheck** →
- **SmartSeal issues receipts consumed by SmartRoute** →

Open [`site/playground.html`](site/playground.html) for the interactive version.

## Part of the Smart* family

One system, not nine projects — same mascot, same manifesto voice, same rule-ID style,
all aligned to the [IAIso standard](https://github.com/SmartTasksOrg/IAIso). Each is an independent, open-source, single-purpose tool you can integrate into your own architecture:

| Tool | IAIso | What it does |
|---|---|---|
| [SmartPangolin](https://github.com/SmartTasksOrg/smartpangolin) | §1 · Secure Sharing | Scan before you share. Stop leaking secrets into AI models, agents, and tools. |
| [SmartPrompt](https://github.com/SmartTasksOrg/smartprompt) | §4 · Context | Lint before you send. Bad prompt in, bad work out — and it's your name on it. |
| [SmartCheck](https://github.com/SmartTasksOrg/smartcheck) | §2 · Verification | Check before you sign off. Catch the AI when it's confidently wrong. |
| [SmartStandard](https://github.com/SmartTasksOrg/smartstandard) | §7 · Standards | Standardize before you scale. One shared, auditable convention for AI-assisted work. |
| [SmartSim](https://github.com/SmartTasksOrg/smartsim) | §8 · Foresight | Simulate before it hits you. See your role's task-by-task collapse sequence. |
| [SmartMoat](https://github.com/SmartTasksOrg/smartmoat) | §6 · Workforce | Know your moat. Score the tasks AI can't easily take — and widen them. |
| [SmartRoute](https://github.com/SmartTasksOrg/smartroute) | §5 · Orchestration | Route only what you trust. Gate agents and tools with trust scores and guardrails. |
| [SmartFeed](https://github.com/SmartTasksOrg/smartfeed) | §9 · Awareness | Distill the firehose. A tight brief of only what moves your work. |

**Backed by the standard:** SmartSeal implements **IAIso §3 · Provenance**.
**Open-source edition:** this repo is the simplified, single-purpose version, built for any org to integrate into its own architecture. SmartTasks' desktop app and [SmartTasks.cloud](https://smarttasks.cloud) run a more advanced, deeply-integrated implementation of the same IAIso governance — a separate product, not this code bundled.

## Who's behind this

- **Roen Branham** — CEO & AI Strategy Architect · CISSP-certified AI, security & governance architect; author of IAIso and sole inventor of the Z4 Semantic Fabric patent application. [LinkedIn](https://www.linkedin.com/in/roen-branham-167ab29/)
- **Le Vu Tanh** — CTO & Core Engineering Lead · Chief architect of the Cortex engine; large-scale system reliability and low-latency infrastructure — the engineer who ships what gets architected. [LinkedIn](https://www.linkedin.com/in/lee-thanh-76aa8ba0/)

The team behind IAIso & SmartTasks: a CISSP-certified security & governance architect
and a large-scale systems engineer — 20+ years shipping secure, AI-driven platforms for
regulated, blue-chip environments (Allianz, BMW, Rolls-Royce, Heidenhain).

<!-- SMARTTASKS-MODELS:START -->
## Runs on governed local models

Each artifact carries a **SHA-256** so you can prove the weights you run match what was tested — content-addressed provenance, like SmartSeal.

This tool is local-first, so pair it with models you can actually vet. **SmartTasks** publishes 21+ governance-validated GGUF builds on Hugging Face — each with a machine-readable **scorecard** (capability tiers L1 Layman → L5 Agentic, IAIso conformance invariants (pass/warn/fail), OWASP-mapped garak red-team, transparency probes (viewpoint-alignment / over-refusal), and per-file SHA-256). Gate model selection on evidence, not vibes — and every finding, including warnings, is published in full.

→ **[SmartTasks on Hugging Face](https://huggingface.co/smarttasks)** · [Qwen3.6-27B](https://huggingface.co/smarttasks/Qwen3.6-27B-GGUF) (L5 agentic) · [react-agent-coder-llama-3.1-8b](https://huggingface.co/smarttasks/react-agent-coder-llama-3.1-8b-GGUF) (agentic coder) · [gpt-oss-20b](https://huggingface.co/smarttasks/gpt-oss-20b-GGUF) (open reasoning)
<!-- SMARTTASKS-MODELS:END -->

## Get in touch

- **Companies & enterprises:** [enterprise@smarttasks.cloud](mailto:enterprise@smarttasks.cloud) — we help
  teams integrate SmartSeal + IAIso into their architecture so governance and
  audit-readiness become a byproduct of how they already work.
- **The standard:** [IAIso](https://github.com/SmartTasksOrg/IAIso) · [iaiso.org](https://iaiso.org)
- **The product:** [SmartTasks.cloud](https://smarttasks.cloud)

Built by **SmartTasks Lab**. Apache-2.0. Contributions welcome.
