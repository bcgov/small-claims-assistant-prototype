# Plugin And Sub-Agent Boundaries

## Purpose

This document defines the first-pass boundary model for the plugin-first Notice of Claim assistant.

The goal is to keep the AI workflow reusable across two future hosts:

- the standalone plugin path
- a later API-backed web app path

These boundaries should describe responsibilities, not implementation language or runtime-specific packaging.

## Boundary Principles

- Keep host-agnostic business tasks separate from runtime-specific orchestration.
- Let sub-agents and skills own reusable decision-making and document-preparation steps.
- Keep deterministic rendering outside the model and inside scripts or services.
- Preserve one canonical case JSON contract between all major components.

## Proposed Layering

### 1. Host Layer

Responsible for how the user reaches the system.

Examples:

- plugin host in an AI tool
- future web app plus API layer

Owns:

- authentication or session entry if needed
- host-specific message display
- handoff into the orchestrating sub-agent

Does not own:

- legal data model
- core question logic
- PDF generation rules

### 2. Orchestrating Sub-Agent

Primary conversational controller for a Notice of Claim session.

Owns:

- managing the intake sequence
- deciding which skill to invoke next
- asking follow-up questions when answers are incomplete
- moving the case toward `ready-for-review` and `ready-for-pdf`

Does not own:

- raw PDF rendering
- final field placement logic
- host-specific UI behavior

### 3. Reusable Skills

These should be designed so they can be called from the plugin now and a web-backed orchestration layer later.

#### `intake-guidance`

Owns:

- explaining court questions in plain language
- clarifying legal or procedural terms
- eliciting missing facts without changing legal meaning

#### `case-normalization`

Owns:

- turning conversational answers into canonical case JSON fields
- enforcing normalized shapes for parties, facts, dates, and remedies

#### `case-validation`

Owns:

- completeness checks
- rule-based warnings
- identifying missing or ambiguous information before generation

#### `pdf-generation`

Owns:

- invoking deterministic scripts
- mapping canonical case JSON into the official PDF package
- reporting generation success or failure

This skill should rely on scripts rather than model prose for output creation.

#### `filing-adapter`

Owns:

- transforming canonical case JSON into a mock or future filing payload
- isolating downstream integration logic from the intake flow

## Recommended Data Flow

```text
Host -> Orchestrating Sub-Agent -> Intake Guidance -> Case Normalization -> Case Validation -> PDF Generation
                                                       \-> Filing Adapter (optional)
```

## What Must Stay Host-Agnostic

- canonical case JSON structure
- rule-based validation logic
- controlled vocabularies and mapping rules
- follow-up question decision rules driven by missing or weak data
- deterministic generation inputs and outputs

## What Can Stay Host-Specific

- chat transcript persistence
- UI components and navigation state
- authentication/session plumbing
- billing, quotas, and provider-specific model routing

## Recommended Script Ownership

Scripts should be owned by reusable skills, not by the top-level host.

Initial expectation:

- Python scripts under a skill-owned `scripts/` folder for PDF generation
- future adapter scripts for filing payload transformation

That keeps deterministic logic portable even if the outer host changes.

## Suggested First Implementation Slice

1. One orchestrating Notice of Claim sub-agent
2. One reusable intake guidance skill
3. One reusable normalization/validation skill pair or combined skill
4. One deterministic PDF generation skill backed by scripts
5. Canonical case JSON passed between all of the above

## Open Boundary Questions

- Should normalization and validation be separate skills or one combined skill in v1?
- Should remedy calculation and attachment overflow logic live in validation or PDF generation?
- How much sub-agent state should be persisted outside canonical case JSON?
- Whether the first plugin implementation needs one orchestrator only or a small hierarchy of specialized sub-agents