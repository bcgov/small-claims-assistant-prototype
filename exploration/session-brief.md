# Exploration Session Brief

## Classification

Domain: software / product feature

Exploration type: greenfield

Prior context: existing system

Desired output: [INTAKE DRAFT - confirm] formal spec and implementation-ready plan for a Notice of Claim-focused AI filing assistant, likely packaged as an installable plugin/skill that can guide a user and produce court-ready outputs

Timebox: [INTAKE DRAFT - confirm] open

## Trigger

User trigger, preserved verbatim:

> "I want to build a small claims forms assistant for BC Courts."

## Prior Context

- There is no existing vibe-coded prototype for this product.
- The current BC reference system is the public Filing Assistant at `https://justice.gov.bc.ca/FilingAssistant/index.do`.
- The existing Filing Assistant was explored using the live browser flow, a mock Notice of Claim run, and screenshots of the generated PDF package.
- The repo is also used secondarily to improve the exploration-cycle plugin and related agent behavior.
- The source of truth for those plugin assets is `C:\Users\RICHFREM\source\repos\agent-plugins-skills\plugins\exploration-cycle-plugin`, not the installed `.agents` copies in this repo.

## Known Constraints

- The first scope is Notice of Claim only.
- The product must eventually output the official BC court form package in the exact document format, not an approximation.
- The Notice of Claim PDF package includes more than one page type: the main Notice of Claim form, attachment pages, and related service/procedural forms.
- Layout fidelity matters: field placement, page structure, line wrapping, totals, checkboxes, and ordering must match the official forms closely enough to be court-ready.
- AI guidance should be used upstream for intake, explanation, drafting help, and validation. Final PDF rendering should remain deterministic.
- The system may need to support more than one output mode:
  - exact Notice of Claim PDF package
  - optional mock or future e-filing API payload/endpoint path
  - canonical case JSON as the machine-readable source-of-truth output
- A future CEIS integration is desirable but should be treated as optional and decoupled from the core intake and PDF-generation path.
- The plugin, skills, and sub-agent should be deployed from a new standalone repository, not from `agent-plugins-skills`.
- The product should support two delivery paths to the same legal output core:
  - an interactive agent skill/plugin path as the preferred initial path
  - a standalone web app as a secondary path with higher hosting and model-cost implications
- Discovery work in this repo should continue to follow the exploration-cycle process and local `.agent/rules` files.
- The plugin/sub-agent route is economically attractive because the AI assistance can use the user's own AI environment and token budget rather than requiring province-hosted model usage.
- A web app with AI clarification support would require hosted API access, infrastructure, and an operating budget for model calls.
- The plugin-first skills and sub-agents should also be treated as a prototype and reuse candidate for any later API-backed AI support in the web app.
- The future web app should follow the BC Government design system rather than a custom design language.
- The shared repo at `temp/repos/claude-design-bc-gov-design-system` provides local reference material for BC Gov tokens, fonts, previews, and component patterns.
- Official BC Gov packages should be treated as the primary source of truth for the web path:
  - `@bcgov/design-system-react-components`
  - `@bcgov/bc-sans`
  - `@bcgov/design-tokens`

## Current Reference System Behavior

- The existing Filing Assistant is a structured web intake flow, not a modern AI system.
- It collects claimant, defendant, incident, venue, date, and remedy information needed for a Notice of Claim.
- It generates a downloadable PDF output package after the flow is completed.
- The Notice of Claim flow includes these major sections:
  - Who are you?
  - Who are you suing?
  - What happened?
  - Where?
  - When?
  - What are you asking for?
  - File
  - Options To Settle
  - Finish

## Evidence Collected So Far

- Mock browser walkthrough of the Notice of Claim flow completed end-to-end.
- Downloaded generated PDF confirmed at `C:\Users\RICHFREM\Downloads\PDF-Output.pdf`.
- Screenshots reviewed for:
  - cover page
  - instructional "Making a Claim" page
  - populated Notice of Claim page
  - attachment page for overflow narrative
  - Certificate of Service page

## Early Direction

[CONFIRMED] The product should support two access paths to the same legal output core, with the interactive plugin/agent skill as the preferred initial path and the web app as a secondary path.

[CONFIRMED] The product should improve the legacy intake experience with guided assistance and stronger validation, while preserving compatibility with the official Notice of Claim output package and leaving room for a future court-filing adapter.

[CONFIRMED] The plugin/sub-agent should be able to explain unclear questions, elaborate on legal or procedural wording, ask follow-up questions, and help users formulate answers before deterministic PDF generation runs.

[INTAKE DRAFT - confirm] A skill-owned scripts folder, likely using Python, is a strong candidate for deterministic PDF generation from canonical case data.

[CONFIRMED] If the web app later adds hosted AI support, it should preferentially reuse the same skills and sub-agents developed for the plugin-first path.

[CONFIRMED] If the web app is built, it should align to the BC Government design system and use the shared BC Gov design repo as a working implementation reference.

## Open Questions

- [INTAKE DRAFT - confirm] Is the desired first milestone a discovery/handoff package, a prototype, or both?
- [CONFIRMED] The first implementation scope should focus on Notice of Claim only.
- [INTAKE DRAFT - confirm] Should CEIS research happen during discovery, or after the PDF-generation baseline is defined?
- [CONFIRMED] The preferred delivery model is plugin-first, with the standalone web app treated as a secondary path.
- [CONFIRMED] The third output mode is canonical case JSON.