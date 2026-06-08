# small-claims-assistant Plugin

Generated via the plugin scaffold workflow and narrowed to the first usable slice: guided Notice of Claim intake for BC Small Claims.

## Purpose
This plugin hosts the plugin-first path for the BC Small Claims assistant. The first slice focuses on interactive intake for Form 1 Notice of Claim, normalizing user answers into the canonical case model that later renderer and validation skills will consume.

The active architecture keeps intake-to-JSON separate from JSON-to-PDF generation so the canonical case contract stays reusable across validation, deterministic rendering, a future filing adapter, and a later BC Gov web application path.

## How users should start

Start with the intake flow. A normal user should begin by asking for help with the Notice of Claim itself, not by naming scripts, JSON, or internal files.

Good starting requests are:

- `Help me fill out a BC Small Claims Notice of Claim.`
- `Start a Notice of Claim intake interview.`
- `I want to make a small claims claim in BC. Walk me through the form.`
- `I have some facts already; help me turn them into a Notice of Claim draft.`

From there, the plugin is meant to route into the `notice-of-claim-intake-agent` using the `notice-of-claim-intake` skill. That intake experience is the front door: it asks a small number of questions at a time, captures party details, claim amount, narrative, dates, remedies, and then asks the user to confirm the summary before moving on.

The intended user flow is:

1. Start by describing the claim in plain English.
2. Let the intake agent guide the interview and collect the missing facts in small batches.
3. Confirm the captured facts when the intake summary is shown.
4. Ask for the next stage only after intake is complete enough.

Typical next-stage requests are:

- `Prepare the draft PDF.`
- `Check whether this is ready for the PDF.`
- `Prepare the filing submission step.`

In practice, users should not need to know the agent or skill names. The natural entry point is a plain-language request such as `Help me start a BC Small Claims Notice of Claim.`

For a shorter user-facing guide, see `START_HERE.md`.

## Current Components

### Agents
- `agents/notice-of-claim-intake-agent.md` — interactive intake sub-agent for guided questioning and canonical-case capture

### Skills
- `skills/notice-of-claim-intake/` — interactive intake skill scaffold for the Notice of Claim interview flow
- `skills/notice-of-claim-pdf-generation/` — deterministic generation skill scaffold for readiness checks and renderer handoff
- `skills/notice-of-claim-filing-adapter/` — deterministic mock filing-adapter scaffold for downstream payload transformation

### Scripts
- `scripts/write_notice_of_claim_json.py` — deterministic writer that merges partial intake data onto the canonical Notice of Claim draft template
- `scripts/render_notice_of_claim_pdf.py` — deterministic renderer entrypoint that validates canonical JSON readiness and emits a PDF artifact manifest
- `scripts/submit_notice_of_claim_mock_api.py` — deterministic filing-adapter entrypoint that emits mock request and response artifacts from canonical JSON

### Data Assets
- `assets/case-models/notice-of-claim/notice-of-claim-intake-definition.json` — observed Filing Assistant question order plus canonical JSON draft template

### Assets
- `assets/templates/forms/small-claims/scl001-notice-of-claim-template.pdf` — authoritative archived Form 1 template used for deterministic rendering work

### Dependency Files
- `requirements-core.in` / `requirements-core.txt` — plugin-level shared Python dependency baseline
- `requirements-pdf.in` / `requirements-pdf.txt` — managed PDF-generation dependency slice for renderer work

## Notes
- `plugin.json` stays minimal for compatibility with the local validator and Claude plugin auto-discovery.
- `plugin.yaml` carries the explicit skill inventory for Hermes-style compatibility.
- The intake skill remains limited to guided intake and canonical JSON updates.
- The PDF-generation slice is intentionally separate so deterministic rendering can evolve without collapsing back into the intake skill.
- The filing-adapter slice is intentionally separate so downstream API payload logic can evolve without collapsing into intake or rendering.

## Backlog Visibility

The broader explored product path remains in view while the current implementation stays narrow:

- reusable skill decomposition beyond v1 intake and generation
- canonical Notice of Claim JSON as the shared source of truth
- deterministic renderer expansion from template scaffold to field binding and overflow handling
- future filing-adapter boundary that consumes canonical JSON
- future BC Gov design-system web app path reusing the same legal-output core

## Directory Structure

```text
small-claims-assistant/
├── .claude-plugin/
│   └── plugin.json
├── __init__.py
├── .claude/
│   └── settings.json
├── agents/
│   └── notice-of-claim-intake-agent.md
├── assets/
│   ├── case-models/notice-of-claim/notice-of-claim-intake-definition.json
│   └── templates/forms/small-claims/scl001-notice-of-claim-template.pdf
├── plugin.yaml
├── requirements-core.in
├── requirements-core.txt
├── requirements-pdf.in
├── requirements-pdf.txt
├── README.md
├── references/
├── tests/
│   └── test_render_notice_of_claim_pdf.py
│   └── test_submit_notice_of_claim_mock_api.py
├── scripts/
│   ├── render_notice_of_claim_pdf.py
│   ├── submit_notice_of_claim_mock_api.py
│   └── write_notice_of_claim_json.py
└── skills/
    └── notice-of-claim-intake/
        ├── SKILL.md
        ├── assets/
        ├── evals/
        │   └── evals.json
        ├── scripts/
        └── references/
            └── acceptance-criteria.md
    └── notice-of-claim-pdf-generation/
        ├── SKILL.md
        └── scripts/
    └── notice-of-claim-filing-adapter/
        ├── SKILL.md
        └── scripts/
```