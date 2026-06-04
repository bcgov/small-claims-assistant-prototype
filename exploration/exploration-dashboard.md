# Business Exploration Dashboard

**Session:** BC Small Claims Forms Assistant
**Session Type:** Greenfield
**Dispatch Strategy:** direct
**Current Phase:** Phase 1 - Problem Framing
**Status:** In Progress

---

## The Exploration Loop

- [ ] **Phase 1: Problem Framing**
  - Skill: `discovery-planning`
  - Gate: SME approval of Discovery Plan
  - Outcome: `exploration/discovery-plans/discovery-plan-YYYY-MM-DD.md`

- [ ] **Phase 2: Visual Blueprinting**
  - Skill: `visual-companion`
  - Gate: SME selection and confirmation of layout direction
  - Outcome: `exploration/captures/layout-direction.md`

- [ ] **Phase 3: Build**
  - Skill: `subagent-driven-prototyping`
  - Gate: SME walkthrough and sign-off on working build
  - Outcome (Greenfield): `exploration/prototype/index.html`

- [ ] **Phase 4: Handoff & Specs**
  - Skill: `exploration-handoff`
  - Gate: SME approval of final handoff package
  - Outcome: `exploration/handoffs/handoff-package.md`

---

## Session Type Guide

| Type | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|------|---------|---------|---------|---------|
| **Greenfield** (new app) | Required | Required | Standalone prototype | Required |
| **Brownfield** (existing app) | Required | Optional | Builds into codebase | Optional |
| **Analysis/Docs** (non-software) | Required | Optional (structure) | Skipped | Required (primary output) |
| **Spike** (investigation) | Required, may repeat | Flexible | Flexible | Optional |

---

## Session Log

| Phase | Completed | Notes |
|-------|-----------|-------|
| Phase 1 | In progress | Reviewed BC Filing Assistant Notice of Claim flow, generated mock PDF package, captured layout evidence from screenshots, narrowed first scope to Notice of Claim only, confirmed a two-path standalone product direction, defined the canonical case JSON as a shared output contract, mapped observed package pages and fields back to that contract, translated that mapping into a renderer implementation checklist, and drafted host-agnostic plugin/sub-agent boundaries for later web API reuse. |
| Phase 2 | - | Not started. |
| Phase 3 | - | Not started. |
| Phase 4 | - | Not started. |