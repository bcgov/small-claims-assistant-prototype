# Repo Instructions

This repository has two active purposes:

1. Build and iterate on a BC Small Claims Forms Assistant prototype (plugin-first, intake-to-PDF pipeline). A working prototype exists at [bcgov/small-claims-assistant-prototype](https://github.com/bcgov/small-claims-assistant-prototype).
2. Improve the exploration-cycle plugin, skills, and agent behavior that support this workflow.

## Sources Of Truth

- The canonical source for the exploration-cycle plugin is:
  `C:\Users\RICHFREM\source\repos\agent-plugins-skills\plugins\exploration-cycle-plugin`
- The installed copies under `.agents/agents`, `.agents/workflows`, and `.agents/skills` in this repo are runtime copies for inspection and local use, not the source of truth.
- If a task involves improving plugin agents, workflows, skills, templates, or references, edit the canonical plugin source first unless the user explicitly asks for a local-only experiment.

## Local Rules Are Mandatory

Always read and follow the relevant files under `.agent/rules/` before making changes in their scope.

Pay particular attention to:

- `.agent/rules/self-evolution-policy.md`
- `.agent/rules/test-driven-development.md`
- `.agent/rules/plugin-architecture-policy.md`
- `.agent/rules/coding-conventions.md`
- `.agent/rules/dependency-management.md`
- `.agent/rules/symlink-cross-platform.md`

If two instructions appear to conflict, prefer the more local rule and then the explicit user request.

## Exploration Workflow Defaults

- Assume Path 1 pre-build discovery unless the user explicitly says there is an existing vibe-coded prototype.
- Do not force Path 2 vibe-rescue behavior when the user has confirmed there is no existing vibe-coded app.
- During intake and early exploration, do not jump straight to implementation planning or code generation unless the user explicitly asks to bypass discovery.
- Treat `exploration/session-brief.md` as the first-class intake artifact for this repo.
- Maintain exploration artifacts as work progresses so the user does not need to ask repeatedly.

## Required Exploration Artifacts

Keep these files current during discovery work:

- `exploration/exploration-dashboard.md`
- `exploration/session-brief.md`
- `exploration/captures/reference-system-findings.md`

Use these rules when updating them:

- Preserve the user's own phrasing for the trigger when possible.
- Mark uncertain items as `[INTAKE DRAFT — confirm]` or `[UNCONFIRMED]`.
- Record observed evidence from screenshots, PDFs, browser walkthroughs, and public references before translating it into product decisions.
- Do not write a formal engineering spec too early; capture evidence and structured discovery first.

## BC Small Claims Product Context

Current standing assumptions for this repo:

- The target product is a BC Small Claims Forms Assistant. A working prototype (`plugins/small-claims-assistant/`) exists with intake, PDF generation, and mock filing adapter.
- The PDF renderer (`render_notice_of_claim_pdf.py`) overlays case data onto the official SCL 001 form template using template-calibrated coordinate constants. Field placement is locked by 13 position-aware automated tests.
- Skill `assets/` directories use file-level symlinks (per plugin architecture policy) to keep each skill self-contained.
- The existing BC Filing Assistant is a reference system, not the product being modified.
- AI belongs upstream in intake, guidance, drafting assistance, and validation. Final form rendering must be deterministic.
- A future CEIS integration may exist as an optional downstream adapter, but it should not be coupled to the core intake and PDF-generation workflow.

## Plugin User Entry Guidance

When explaining how to use the `plugins/small-claims-assistant/` plugin, direct users to start with the intake flow in plain English rather than naming scripts, JSON, or internal files.

Use examples such as:

- `Help me fill out a BC Small Claims Notice of Claim.`
- `Start a Notice of Claim intake interview.`
- `I want to make a small claims claim in BC. Walk me through the form.`
- `I have some facts already; help me turn them into a Notice of Claim draft.`

The expected sequence is:

1. Start with the Notice of Claim itself.
2. Route into intake first.
3. Gather facts in short batches and confirm the summary.
4. Only then move to PDF generation or filing-preparation steps.

Good next-stage requests after intake confirmation are:

- `Prepare the draft PDF.`
- `Check whether this is ready for the PDF.`
- `Prepare the filing submission step.`

Treat `plugins/small-claims-assistant/START_HERE.md` as the user-facing quick-start reference for this flow.

## Plugin Improvement Context

- This repo may be used to refine prompts, skills, and agent behavior for the exploration-cycle plugin.
- When learning something important about the exploration workflow, document it in repo artifacts and, when appropriate, propagate the improvement back to the canonical plugin source.
- Do not treat installed copies as the authoritative place to fix long-term behavior.