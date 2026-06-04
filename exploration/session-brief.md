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
  - [INTAKE DRAFT - confirm] a third structured machine-readable output such as canonical case JSON or filing package data
- A future CEIS integration is desirable but should be treated as optional and decoupled from the core intake and PDF-generation path.
- The product is now intended to live in this standalone repository, not in `agent-plugins-skills`.
- The product should support two delivery paths to the same legal output core:
  - a standalone web app
  - an interactive agent skill/plugin hosted in this repo
- Discovery work in this repo should continue to follow the exploration-cycle process and local `.agent/rules` files.

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

[CONFIRMED] The product should support two access paths in parallel: a standalone web app and an interactive plugin/agent skill, both reaching the same legal output core.

[INTAKE DRAFT - confirm] The product should improve the legacy intake experience with guided assistance and stronger validation, while preserving compatibility with the official Notice of Claim output package and leaving room for a future court-filing adapter.

## Open Questions

- [INTAKE DRAFT - confirm] Is the desired first milestone a discovery/handoff package, a prototype, or both?
- [CONFIRMED] The first implementation scope should focus on Notice of Claim only.
- [INTAKE DRAFT - confirm] Should CEIS research happen during discovery, or after the PDF-generation baseline is defined?
- [CONFIRMED] The preferred delivery model includes both a standalone web app and an interactive plugin/agent skill path.
- [INTAKE DRAFT - confirm] What is the intended third output mode in addition to PDF and optional e-filing/API output?