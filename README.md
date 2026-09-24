# Jev CogSec Spike

A deliberately small A/B experiment for **cognitive security (CogSec)** in agentic systems.

The experiment runs two otherwise-identical Google ADK agents on the same eval suites:

- **baseline**: Gemini 3.5 Flash-Lite + normal prompt-level instruction hierarchy.
- **guarded**: the same agent, plus a Jev System One gate that inspects untrusted web content returned by tools before it is sent back to the LLM.

The first target is **indirect prompt injection in web content**.

> Hypothesis: a fast typed System One classifier can act as a cognitive-security sensor, while deterministic code decides whether to allow or quarantine retrieved content.

The repository is intentionally tiny. No UI, database, real network fetcher, or production security claims. The web tool uses deterministic local fixtures so both variants see exactly the same content and ADK evals can be replayed.

## Experiment shape

```text
same user prompt
      |
      +-------------------------+
      |                         |
 baseline                  guarded
      |                         |
 Gemini 3.5 Flash-Lite     web tool result
      |                         |
 web fixture                 Jev gate
      |                         |
 model sees page            allow/quarantine
      |                         |
      +------ ADK evals --------+
```

The same system instruction tells both agents that web content is untrusted data and must never override user/system instructions. The guarded variant adds only the Jev gate, giving us a cleaner A/B than comparing a naive prompt against a guarded agent.

## What we measure

- successful completion of benign web tasks;
- resistance to indirect prompt injection;
- unauthorized/surprising tool calls;
- false positives on security-related but benign pages;
- latency overhead of the Jev gate;
- ADK eval trajectories and final-response quality.

## Stack

- Google Agent Development Kit (ADK)
- Gemini 3.5 Flash-Lite
- TypeSafe AI / Jev System One
- ADK eval sets

Implementation lives on a feature branch / PR.
