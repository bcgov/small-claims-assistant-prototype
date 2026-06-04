# Repo Instructions

This repository has two active purposes:

1. Explore and define a BC Small Claims Forms Assistant.
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

- The target product is a BC Small Claims Forms Assistant.
- The existing BC Filing Assistant is a reference system, not the product being modified.
- The product must eventually generate court-ready PDFs that match the official BC form package exactly, not approximately.
- AI belongs upstream in intake, guidance, drafting assistance, and validation. Final form rendering must be deterministic.
- A future CEIS integration may exist as an optional downstream adapter, but it should not be coupled to the core intake and PDF-generation workflow.

## Plugin Improvement Context

- This repo may be used to refine prompts, skills, and agent behavior for the exploration-cycle plugin.
- When learning something important about the exploration workflow, document it in repo artifacts and, when appropriate, propagate the improvement back to the canonical plugin source.
- Do not treat installed copies as the authoritative place to fix long-term behavior.