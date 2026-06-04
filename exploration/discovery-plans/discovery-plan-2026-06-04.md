# Discovery Plan

**Date:** 2026-06-04
**Session:** BC Small Claims Forms Assistant
**Session Type:** Greenfield
**Status:** Draft - awaiting SME approval

---

## Problem Statement

People who need to prepare a BC Small Claims Notice of Claim currently rely on a legacy Filing Assistant that gathers the right information and produces a court-style PDF package, but it is not AI-native, does not provide modern guided assistance, and leaves much of the classification, drafting, and validation burden on the user.

The opportunity is to create a guided AI filing assistant for Notice of Claim that preserves the official output contract while improving the intake and validation experience.

---

## Discovery Goal

Define the first implementation slice for a Notice of Claim-focused assistant that can produce court-ready outputs through a plugin-first AI experience, while preserving the option of a later web application path in the same standalone repository.

The near-term goal is not to give both channels equal weight. The immediate opportunity is to use an interactive agent/plugin skill path as the primary experience because it can rely on the user's own model access and tokens for clarification, drafting help, and question-by-question guidance.

The web application path remains strategically valuable, but it should be treated as a secondary path until the hosting, API, and ongoing model-cost implications are better understood.

---

## Confirmed Scope For This Slice

- Form scope is Notice of Claim only.
- The repository is standalone and is not part of `agent-plugins-skills`.
- The preferred initial AI-enabled experience is an interactive agent skill/plugin hosted in this repo.
- A standalone web app remains in scope as a secondary delivery path, not the initial primary investment.
- The generated PDF must match the official BC Notice of Claim package format exactly enough to be court-ready.
- The plugin/agent path should be able to guide users interactively through each question, explain legal or procedural wording, help users elaborate when they are unsure, and reduce the need for external searching.
- The final PDF generation step should be implemented deterministically, likely through embedded scripts under a skill-owned scripts folder rather than through model-generated document output.
- The initial plugin skills and sub-agents should be designed as reusable AI workflow assets, not one-off channel-specific logic.

---

## Candidate Outputs

### Output 1: Official PDF Package

- Exact Notice of Claim PDF package
- Includes fixed-layout pages and attachment-page handling for overflow narrative where needed

### Output 2: Filing Adapter Output

- Mock e-filing API endpoint interaction or filing payload output
- Future-ready placeholder for CEIS-style integration

### Output 3: Structured Machine Output

- Canonical case JSON as the machine-readable source-of-truth export
- This JSON should represent the normalized Notice of Claim data collected during guided intake
- It should be suitable for reuse by the PDF renderer, validation rules, and future filing-adapter integrations

---

## Why This Is The Right Intervention

This remains a software problem, not just a process rewrite, because the current reference system already demonstrates that users need structured guided intake plus a deterministic official form output. The improvement target is not to replace the legal output contract, but to modernize how users reach it and how multiple delivery channels can share the same legal-document core.

The strongest initial intervention is the plugin/sub-agent path because it unlocks AI guidance without shifting model-serving costs to the province. In a web app, every clarification turn, explanation, or drafting assist would require hosted model access, API design, and an operational budget. In a plugin-hosted agent flow, those AI interactions can ride on the user's own AI tooling and token budget while the repo focuses on deterministic legal-output generation.

---

## Shared Core Assumption

Both delivery paths should converge on one shared core:

- canonical Notice of Claim case schema
- validation rules and drafting assistance hooks
- deterministic PDF renderer for official output
- optional filing adapter layer

The delivery channel should change the interaction mode, not the legal-output logic. The plugin/sub-agent path should be the first consumer of that core. The web app should be treated as a later host that can reuse the same schema, validation, and renderer once API and operating-cost questions are resolved.

The same principle should apply to the AI layer where practical: the skills and sub-agents developed for the plugin-first path should also serve as the prototype for future web-app AI support, so later API-backed web assistance can reuse the same conversational guidance patterns, clarification logic, and task boundaries rather than starting over.

---

## Plugin-First Product Rationale

- The legacy assistant was built before modern AI assistance was practical.
- A sub-agent can guide the user through the form interactively rather than forcing them to interpret every court prompt unaided.
- When a user does not understand a question, the agent can explain the term, clarify what the court is asking for, ask follow-up questions, and help the user formulate a response.
- This reduces the current pattern of users leaving the flow to search the web for definitions or examples.
- A skill can own embedded scripts, such as Python utilities under a scripts subfolder, to transform the canonical case data into a deterministic filled PDF package.
- This pattern separates AI assistance from document rendering: the model helps gather and clarify the inputs, while scripts generate the final output.
- Those same skills and sub-agents should be treated as the first prototype of a reusable AI orchestration layer that could later be exposed behind a web application API if the province chooses to fund hosted AI support.

---

## Web App Constraints

- A web app is still possible, but AI assistance there would likely require province-funded API access and hosting.
- Each clarification turn in a hosted web flow would create direct model costs.
- The web path also introduces infrastructure, authentication, API governance, and operational support questions that the plugin-first path can avoid at the start.
- If a web app is added later, the preferred path is to reuse the same skills, sub-agents, and decision boundaries already proven in the plugin flow, exposing them through an API-capable application layer rather than inventing a second AI workflow stack.
- For that reason, the web app should be treated as a later expansion or parallel non-AI baseline unless a clear funding and operating model is defined.

---

## First-Round Design Questions

1. Should the first milestone produce only discovery/spec artifacts, or should it also scaffold the plugin/sub-agent path immediately?
2. What is the minimum web-app commitment we want in the first slice: deferred entirely, documented only, or scaffolded without hosted AI?
3. Do we want one shared rendering library consumed by both paths, or one local renderer implementation embedded in each path?
4. What parts of the plugin-first skills and sub-agents should be kept host-agnostic from day one so they can later power API-backed web assistance?

---

## Proposed Next Phase Work

If this plan is approved, the next discovery work should be:

1. Define the canonical Notice of Claim data model
2. Map the required PDF package fields and page behaviors
3. Define the plugin/sub-agent interaction architecture and skill boundaries
4. Define the canonical case JSON contract that becomes the shared machine-readable output
5. Identify which skills, sub-agents, and scripts should be designed for later reuse by a web-app API layer
6. Decide whether to scaffold the standalone repo structure for the plugin-first path immediately and document the web path separately

---

## Approval Gate

No prototype or implementation scaffolding should be treated as the official path forward until this Discovery Plan is explicitly approved by the SME.

**SME approval status:** [PENDING]