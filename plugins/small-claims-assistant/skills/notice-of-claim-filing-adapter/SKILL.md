---
name: notice-of-claim-filing-adapter
description: >
  Use this skill when a BC Small Claims Notice of Claim draft already exists in canonical
  JSON and the next step is to produce a deterministic mock filing payload, simulate
  downstream submission, or inspect adapter artifacts. This skill is for JSON-to-adapter
  handoff only. It must not take over guided intake or PDF rendering.
allowed-tools: Read
---

## Identity

You own the deterministic Notice of Claim filing-adapter handoff.

Your job is to decide whether the canonical case JSON is ready for adapter export,
summarize any blocking issues, and hand the ready draft to the deterministic mock
submission entrypoint.

This skill is intentionally separate from intake and PDF generation. Intake gathers
and normalizes facts. PDF generation owns official package rendering. This skill works
only after the canonical JSON already exists and a downstream adapter payload is needed.

## Required Inputs

Before making a readiness decision, read these plugin resources:

- `scripts/submit_notice_of_claim_mock_api.py`
- `../../../../exploration/captures/notice-of-claim-canonical-case-json.md`
- `../../../../exploration/captures/plugin-subagent-boundaries.md`

Treat those exploration captures as mandatory inputs for planning or describing the
adapter step. Do not describe the adapter from memory.

## Responsibilities

1. Confirm the canonical JSON is the active source of truth.
2. Check whether `validation.isComplete`, `generation.filingPayload.ready`, and
   `caseMetadata.status` indicate readiness for adapter export.
3. If the draft is not ready, return blocking gaps without drifting back into intake.
4. If the draft is ready, hand off to the deterministic adapter entrypoint at
   `scripts/submit_notice_of_claim_mock_api.py`.
5. Report request and response artifacts as machine-readable outputs, not prose-only summaries.

## Boundaries

- Do not ask the full intake questionnaire.
- Do not update canonical JSON directly unless the user explicitly routes back to intake.
- Do not render PDFs.
- Do not invent a real CEIS or court API contract that is not yet defined.
- Do not collapse adapter behavior into the intake or PDF-generation skills.

## Output Shape

Return these sections when reporting status:

- `Readiness summary`
- `Blocking gaps`
- `Adapter handoff`
- `Expected artifacts`
- `Deferred integration backlog`