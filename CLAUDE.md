# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repo has two active purposes:
1. Build a BC Small Claims Forms Assistant (plugin-first, intake-to-PDF pipeline).
2. Improve the `exploration-cycle` plugin, skills, and agent behavior that supports this workflow.

## Local Rules

Always read the relevant rule file under `.agent/rules/` before making changes in its scope. The most important:

- `.agent/rules/test-driven-development.md` — no implementation without a failing test first
- `.agent/rules/coding-conventions.md` — dual-layer docs, file headers, type hints, 50-line/3-nesting refactor threshold
- `.agent/rules/plugin-architecture-policy.md`
- `.agent/rules/dependency-management.md` — never `pip install` directly; use `.in` → `pip-compile` → `.txt`
- `.agent/rules/symlink-cross-platform.md`

If rules conflict, prefer the more local rule, then the explicit user request.

## Running Tests

```powershell
# Run all plugin tests
python -m pytest plugins/small-claims-assistant/tests/ -v

# Run a single test file
python -m pytest plugins/small-claims-assistant/tests/test_render_notice_of_claim_pdf.py -v

# Run a single test by name
python -m pytest plugins/small-claims-assistant/tests/test_render_notice_of_claim_pdf.py::test_function_name -v
```

Install PDF dependencies before running renderer tests:
```powershell
pip install -r plugins/small-claims-assistant/requirements-pdf.txt
```

## Plugin Architecture

The `plugins/small-claims-assistant/` plugin is the active implementation. Its architecture enforces a strict separation of concerns:

```
Intake (agent/skill) → canonical JSON → renderer script → PDF artifact
                                      → filing-adapter script → mock API payload
```

- **`agents/notice-of-claim-intake-agent.md`** — interactive intake sub-agent; drives guided questioning and writes canonical case JSON
- **`scripts/write_notice_of_claim_json.py`** — merges partial intake data onto the canonical draft template
- **`scripts/render_notice_of_claim_pdf.py`** — validates canonical JSON readiness and overlays field data onto `scl001-notice-of-claim-template.pdf` using `pypdf` + `reportlab`
- **`scripts/submit_notice_of_claim_mock_api.py`** — filing-adapter stub that emits mock request/response artifacts from canonical JSON
- **`assets/case-models/notice-of-claim/notice-of-claim-intake-definition.json`** — canonical case model schema and draft template; the shared contract between intake, rendering, and the filing adapter

AI involvement ends at intake and validation. PDF rendering must be deterministic — no AI in the render path.

## Exploration Artifacts

Keep these files current during discovery work:

- `exploration/exploration-dashboard.md`
- `exploration/session-brief.md`
- `exploration/captures/reference-system-findings.md`

The `exploration/session-brief.md` is the first-class intake artifact. Do not write a formal engineering spec before capturing evidence and structured discovery first. Mark uncertain items as `[INTAKE DRAFT — confirm]` or `[UNCONFIRMED]`.

## Canonical Plugin Source

The canonical source for the `exploration-cycle` plugin is:
`C:\Users\RICHFREM\source\repos\agent-plugins-skills\plugins\exploration-cycle-plugin`

The installed copies under `.agents/` in this repo are runtime copies for inspection and local use — not the source of truth. When improving plugin agents, skills, or templates, edit the canonical source first unless the user explicitly asks for a local-only experiment.

## Product Constraints

- The product must generate court-ready PDFs that match the official BC form package **exactly** — approximate rendering is not acceptable.
- AI belongs upstream (intake, guidance, drafting, validation). Final form rendering must be deterministic.
- A future CEIS integration is an optional downstream adapter and must not be coupled to the core intake and PDF-generation workflow.
- The existing BC Filing Assistant is a **reference system**, not the product being modified.
