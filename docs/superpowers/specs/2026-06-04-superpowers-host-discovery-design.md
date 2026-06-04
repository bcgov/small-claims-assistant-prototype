# Exploration Outputs To Superpowers Design

## Summary

This design replaces the too-narrow host-discovery-only framing with the actual session scope.

The problem is not only that exploration-cycle wording assumed the wrong Superpowers install shape. The larger issue is that the exploration outputs produced in this repo were not carried forward into a complete Superpowers-ready spec and implementation plan. That broke the bridge between exploration and execution.

This design defines that bridge explicitly.

It treats the exploration artifacts in `exploration/` as required upstream inputs for downstream Superpowers planning and implementation, and it keeps the full discussed output set in scope:

- plugin-first agent experience
- reusable skills
- deterministic scripts
- canonical case JSON
- official PDF package rendering
- future filing-adapter/API boundary
- future BC Gov design system web app path
- workflow fixes so future sessions do not lose those outputs during handoff

## Diagnosis

Two things are true at once.

### 1. Execution failed in this session

I narrowed the written spec and plan to one documentation slice instead of propagating the exploration outputs that had already been captured in:

- `exploration/session-brief.md`
- `exploration/discovery-plans/discovery-plan-2026-06-04.md`
- `exploration/captures/plugin-subagent-boundaries.md`
- `exploration/captures/notice-of-claim-canonical-case-json.md`
- `exploration/captures/notice-of-claim-pdf-field-mapping.md`
- `exploration/captures/notice-of-claim-renderer-implementation-checklist.md`
- `exploration/captures/reference-system-findings.md`

That is an execution miss.

### 2. The source workflow also has a handoff gap

The exploration-cycle source does produce handoff and planning-draft stages, but the contract is still too implicit for the Superpowers path.

The current workflow makes it possible to produce:

- an exploration handoff package
- a spec draft
- a plan draft
- a tasks outline

But it does not explicitly require that a downstream Superpowers spec/plan consume the exploration artifact inventory as mandatory inputs, nor does it make that artifact-to-plan traceability a first-class rule. That leaves too much room for a worker to plan from memory or from the most recent slice instead of from the accumulated exploration record.

So the answer is: **the immediate failure was execution, and there is also a source-agent design gap worth fixing.**

## Inputs That Must Feed Superpowers Planning

The following artifacts are required inputs for the downstream Superpowers spec and plan.

### Core exploration artifacts

- `exploration/session-brief.md`
- `exploration/discovery-plans/discovery-plan-2026-06-04.md`
- `exploration/exploration-dashboard.md`

### Domain and architecture captures

- `exploration/captures/reference-system-findings.md`
- `exploration/captures/plugin-subagent-boundaries.md`
- `exploration/captures/notice-of-claim-canonical-case-json.md`
- `exploration/captures/notice-of-claim-pdf-field-mapping.md`
- `exploration/captures/notice-of-claim-renderer-implementation-checklist.md`

### Current implementation slice artifacts already created

- `plugins/small-claims-assistant/.claude-plugin/plugin.json`
- `plugins/small-claims-assistant/plugin.yaml`
- `plugins/small-claims-assistant/__init__.py`
- `plugins/small-claims-assistant/agents/notice-of-claim-intake-agent.md`
- `plugins/small-claims-assistant/skills/notice-of-claim-intake/SKILL.md`
- `plugins/small-claims-assistant/assets/case-models/notice-of-claim/notice-of-claim-intake-definition.json`
- `plugins/small-claims-assistant/scripts/write_notice_of_claim_json.py`

### Workflow-improvement slice artifacts

- `.agents/skills/exploration-workflow/SKILL.md`
- `.agents/skills/exploration-workflow/references/phase3-execution-discipline.md`
- the canonical exploration-cycle source equivalents in the source-of-truth plugin repo

## Goals

1. Make the Superpowers spec and plan reflect the full discussed product and output set, not only one workflow-doc defect.
2. Keep the Notice of Claim product architecture visible in the plan: agent, reusable skills, deterministic scripts, canonical JSON, renderer, future filing adapter, and future web app.
3. Fix the exploration-to-Superpowers handoff so exploration outputs become required planning inputs rather than optional context.
4. Preserve the plugin-first delivery strategy while keeping the web app and API path explicitly modeled as later consumers of the same core.
5. Define a clean implementation boundary for the next session so work can continue without re-discovery.
6. Use relative repo paths in the written artifacts rather than machine-local absolute paths.

## Non-Goals

1. Building the full Notice of Claim product in this session.
2. Implementing the full web app in this session.
3. Designing a live court-filing integration in this session.
4. Replacing the exploration-cycle workflow with a different planning system.

## Desired Outputs

This session's planning artifacts must cover all of these outputs, even when some are deferred to later implementation slices.

### Output Group A: Shared product core

1. One canonical Notice of Claim case contract, represented by the explored canonical JSON.
2. One deterministic write/update path for case JSON.
3. One deterministic renderer path for the official Notice of Claim package.
4. One validation boundary between conversational intake and generation.
5. One optional future filing-adapter/API boundary that consumes canonical JSON rather than bypassing it.

### Output Group B: Plugin-first AI path

1. One orchestrating Notice of Claim sub-agent.
2. Reusable skills for intake guidance, normalization, validation, generation, and later filing-adapter behavior.
3. Skill-owned or plugin-owned deterministic scripts invoked by skills rather than by ad hoc host logic.
4. Plugin packaging that uses shared root assets/scripts/references with skill-local file links where required.

### Output Group C: Deterministic Python generation slice

1. A separate JSON-to-PDF generation capability rather than overloading the intake skill.
2. Likely a separate `pdf-generation` skill that consumes canonical JSON and invokes deterministic Python code.
3. Python PDF dependencies managed under the local dependency-management rule:
	- no ad hoc `pip install`
	- use `.in` plus compiled `.txt`
	- keep dependency intent and lockfiles together
	- keep shared scripts at plugin root and expose them through skill-local links where needed
4. A plugin-level requirements layout that supports deterministic generation without violating service sovereignty or the hub-and-spoke script rule.

### Output Group D: Future web-app path

1. A BC Gov design-system-aligned web app path.
2. Reuse of the same canonical JSON, validation rules, and deterministic renderer.
3. A future hosted-AI boundary that can reuse the plugin-first orchestration design rather than inventing a second workflow stack.

### Output Group E: Workflow and planning outputs

1. A Superpowers-ready design doc that is explicitly fed by exploration artifacts.
2. A detailed implementation plan for the next clean session.
3. A living task decomposition that separates current slice, next slice, and deferred items.
4. Validation and audit outputs for workflow guidance and the active plugin slice.
5. A clean-session handoff boundary so implementation can begin without re-deriving the product model.

## Recommended Structure

The work should be treated as two connected workstreams.

### Workstream 1: Product architecture continuity

This workstream keeps the real product in view.

It carries forward the explored decisions that:

- the first scope is Notice of Claim only
- the preferred initial delivery path is plugin-first
- the legal-output core is shared across channels
- the canonical JSON is the machine-readable source of truth
- deterministic generation owns final form output
- the web app is secondary but intentionally designed for later reuse
- the API and filing adapter are future-facing and decoupled
- JSON creation and PDF generation are separate deterministic capabilities and may be owned by separate skills

### Workstream 2: Exploration-to-Superpowers handoff discipline

This workstream fixes the planning and orchestration gap.

It must ensure that:

- exploration artifacts are inventoried before downstream planning starts
- Superpowers planning consumes those artifacts explicitly
- planning does not collapse to the last edited slice
- the task ledger stays current as scope evolves
- the source exploration workflow gives future workers a stronger handoff contract

## Product Architecture Decisions To Preserve

### Delivery model

The product is plugin-first, web-second.

The plugin-first path is the preferred first build because it can use the user's own AI runtime and token budget for guidance, clarification, and drafting help. The web path remains in scope, but it introduces hosting, API, and operating-cost questions that are not required to prove the core product.

### Shared core

Both channels must converge on the same shared legal-output core:

- canonical Notice of Claim case JSON
- rule-based validation and readiness checks
- deterministic renderer for official package output
- optional filing adapter layer

### AI boundary

AI belongs upstream in intake, clarification, explanation, normalization help, and validation support.

AI does not own final PDF generation.

### Reusable skill model

The plugin path should evolve toward a reusable skill layout consistent with the explored boundaries:

- `intake-guidance`
- `case-normalization`
- `case-validation`
- `pdf-generation`
- `filing-adapter`

The current `notice-of-claim-intake` slice is an early implementation slice, not the final decomposition.

### Scripts and deterministic code

Deterministic scripts should live in reusable plugin-owned or skill-owned script surfaces, not in prompt text.

Current example already in scope:

- `plugins/small-claims-assistant/scripts/write_notice_of_claim_json.py`

Future deterministic script surfaces must cover:

- renderer entrypoint
- template and page assembly
- overflow handling
- optional filing-payload transformation

The JSON writer and the PDF renderer should be treated as separate deterministic Python capabilities, even if they share a plugin-level package or requirements family.

### Python dependency-management rule

The deterministic generation slice must follow `.agent/rules/dependency-management.md`.

That means:

- no manual `pip install`
- dependency changes flow through `.in` to compiled `.txt`
- dependency intent and lockfiles must be committed together
- shared scripts stay canonical at plugin root
- installed skills must remain self-contained after installation

### Web app and API path

The future web app should:

- follow the BC Government design system
- use the explored BC Gov packages as the visual source of truth
- reuse the same shared legal-output core
- optionally expose the same conversational guidance patterns through an API-backed orchestration layer later

## Workflow Fix Required In The Source Plugin

The exploration-cycle source should be improved so that when exploration is narrowed enough for downstream planning, the workflow does not merely produce a generic handoff and drafts. It should also make the following rules explicit:

1. The downstream planner must inventory the relevant exploration artifacts.
2. The generated spec and plan must trace back to those artifacts.
3. If the SME has corrected scope or output expectations, the planning task list must be rewritten before implementation starts.
4. Superpowers-backed planning should keep current, next, and deferred slices visible rather than collapsing them into one narrow patch plan.
5. If the product architecture implies distinct deterministic capabilities, such as JSON writing and JSON-to-PDF rendering, the plan must preserve those as separate outputs or explicitly justify combining them.

This is the source-agent flaw worth fixing.

## Validation Requirements

Validation for this design slice is document and traceability focused.

1. Confirm the written spec names the exploration artifacts that feed the Superpowers plan.
2. Confirm the written spec includes the discussed product outputs: agent, skills, separate deterministic JSON writer and PDF generation capability, canonical JSON, renderer, web app path, and API or filing-adapter path.
3. Confirm the written spec explicitly diagnoses both the execution miss and the source-workflow handoff gap.
4. Confirm the implementation plan is broken into clean-session implementation slices rather than only the host-discovery wording fix.
5. Confirm the plan and spec use repo-relative paths instead of machine-local absolute paths.

## Expected Outcome

After this rewrite, the written Superpowers spec should be broad enough to support the next clean implementation session without re-discovery.

It should also leave a clear judgment:

- **This session's planning miss was primarily an execution failure.**
- **The exploration-cycle source still needs a stronger artifact-to-Superpowers handoff contract so the same miss is harder to repeat.**

1. A Superpowers-ready design doc explicitly fed by exploration artifacts.
2. A detailed implementation plan for the next clean session.
3. A living task decomposition separating current, next, and deferred slices.
4. Validation and audit outputs for workflow guidance and the active plugin slice.
5. A clean-session handoff boundary so implementation can begin without re-discovery.

## Product Architecture Decisions To Preserve

### Delivery model

The product is plugin-first and web-second.

The plugin-first path is the preferred first build because it can use the user's own AI runtime and token budget for guidance, clarification, and drafting help. The web path remains intentionally in scope, but it introduces hosting, API, and operating-cost questions that are not required to prove the legal-output core.

### Shared core

Both channels must converge on the same shared legal-output core:

- canonical Notice of Claim case JSON
- rule-based validation and readiness checks
- deterministic generation for the official package
- optional filing-adapter layer

### AI boundary

AI belongs upstream in intake, clarification, explanation, normalization help, and validation support.

AI does not own final court-form rendering.

### Reusable skill model

The plugin path should evolve toward a reusable skill layout consistent with the explored boundaries:

- `intake-guidance`
- `case-normalization`
- `case-validation`
- `pdf-generation`
- `filing-adapter`

The current `notice-of-claim-intake` skill is an early intake slice, not the final decomposition.

### Separate PDF-generation capability is required

The current intake skill correctly points to the canonical JSON definition and the JSON writer script, but that is only the intake-to-JSON half of the architecture.

The explored product also needs a separate deterministic capability that reads canonical JSON and emits the official PDF package.

That capability should be represented as either:

1. a dedicated `pdf-generation` skill, or
2. a Notice-of-Claim-specific generation skill such as `notice-of-claim-pdf-generation`.

In either case, it should be separate from the intake skill because the responsibilities are different:

- intake skill: ask questions, normalize answers, update canonical JSON
- generation skill: validate readiness, invoke deterministic Python code, and emit PDF artifacts

### Python dependency policy for PDF generation

The JSON-to-PDF path will require Python PDF libraries. Those dependencies must follow `.agent/rules/dependency-management.md`.

That means:

1. no ad hoc `pip install`,
2. dependency changes go through `.in` to compiled lockfiles,
3. intent and lockfiles are committed together,
4. shared deterministic code remains rooted at the plugin level,
5. installed skills must end up self-contained after installation.

The spec therefore needs to carry both the separate generation skill and the separate dependency-managed Python surface.

### Scripts and deterministic code

Deterministic scripts should live in reusable plugin-owned or skill-owned script surfaces, not in prompt text.

Current example already in scope:

- `plugins/small-claims-assistant/scripts/write_notice_of_claim_json.py`

Future deterministic script surfaces must cover:

- renderer entrypoint
- template/page assembly
- overflow handling
- optional filing-payload transformation

### Web app and API path

The future web app should:

- follow the BC Government design system,
- reuse the same canonical JSON, validation rules, and deterministic generation core,
- optionally expose the same conversational guidance patterns through an API-backed orchestration layer later.

## Workflow Fix Required In The Source Plugin

The exploration-cycle source should be improved so that when exploration is narrowed enough for downstream planning, the workflow does not merely produce generic handoff and draft artifacts. It should also make these rules explicit:

1. the downstream planner must inventory the relevant exploration artifacts,
2. the generated Superpowers design and plan must trace back to those artifacts,
3. if the SME changes output expectations or scope, the task ledger must be rewritten before implementation resumes,
4. current, next, and deferred outputs must remain visible rather than collapsing into one narrow patch plan.

This is the source-agent flaw worth fixing.

## Validation Requirements

1. Confirm the written design names the exploration artifacts that feed the Superpowers plan.
2. Confirm the written design includes the discussed outputs: agent, reusable skills, deterministic scripts, canonical JSON, separate PDF generation, future web app, and future API/filing-adapter path.
3. Confirm the written design explicitly diagnoses both the execution miss and the source-workflow handoff gap.
4. Confirm the implementation plan is broken into clean-session implementation slices rather than only the host-discovery wording fix.
5. Confirm the design and plan use repo-relative paths instead of machine-local absolute paths.

## Expected Outcome

After this rewrite, the Superpowers design should be broad enough to support the next clean implementation session without re-discovery.

It should also leave a clear judgment:

- **This session's planning miss was primarily an execution failure.**
- **The exploration-cycle source still needs a stronger artifact-to-Superpowers handoff contract so the same miss is harder to repeat.**