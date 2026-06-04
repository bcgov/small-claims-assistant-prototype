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

Define the first implementation slice for a Notice of Claim-focused assistant that can produce court-ready outputs through two delivery paths in a standalone repository:

1. A web application path
2. An interactive agent/plugin skill path

Both paths should be able to reach the same end outputs through a shared canonical case model and deterministic rendering logic.

---

## Confirmed Scope For This Slice

- Form scope is Notice of Claim only.
- The repository is standalone and is not part of `agent-plugins-skills`.
- The assistant should support at least two product access paths:
  - standalone web app
  - interactive agent skill/plugin hosted in this repo
- The generated PDF must match the official BC Notice of Claim package format exactly enough to be court-ready.

---

## Candidate Outputs

### Output 1: Official PDF Package

- Exact Notice of Claim PDF package
- Includes fixed-layout pages and attachment-page handling for overflow narrative where needed

### Output 2: Filing Adapter Output

- Mock e-filing API endpoint interaction or filing payload output
- Future-ready placeholder for CEIS-style integration

### Output 3: Structured Machine Output

- [UNCONFIRMED] Canonical case JSON, filing package JSON, or equivalent machine-readable export

---

## Why This Is The Right Intervention

This remains a software problem, not just a process rewrite, because the current reference system already demonstrates that users need structured guided intake plus a deterministic official form output. The improvement target is not to replace the legal output contract, but to modernize how users reach it and how multiple delivery channels can share the same legal-document core.

---

## Shared Core Assumption

Both delivery paths should converge on one shared core:

- canonical Notice of Claim case schema
- validation rules and drafting assistance hooks
- deterministic PDF renderer for official output
- optional filing adapter layer

The delivery channel should change the interaction mode, not the legal-output logic.

---

## First-Round Design Questions

1. What is the exact third output mode besides PDF and mock/direct filing?
2. Should the first milestone produce only discovery/spec artifacts, or should it also scaffold both delivery paths?
3. Should the plugin/agent path be treated as the primary user experience, with the web app as a secondary host, or should both be first-class from day one?
4. Do we want one shared rendering service/library consumed by both paths, or one local renderer implementation embedded in each path?

---

## Proposed Next Phase Work

If this plan is approved, the next discovery work should be:

1. Define the canonical Notice of Claim data model
2. Map the required PDF package fields and page behaviors
3. Define the two delivery-path architecture
4. Confirm the third output mode
5. Decide whether to scaffold the standalone repo structure for both paths immediately

---

## Approval Gate

No prototype or implementation scaffolding should be treated as the official path forward until this Discovery Plan is explicitly approved by the SME.

**SME approval status:** [PENDING]