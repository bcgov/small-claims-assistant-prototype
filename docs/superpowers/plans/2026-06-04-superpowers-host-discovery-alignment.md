# Exploration Outputs To Superpowers Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the exploration artifacts and current implementation slices into a complete Superpowers-ready planning baseline, then implement the workflow and plugin changes needed so a fresh session can continue from a clean handoff instead of re-discovery.

**Architecture:** Split the work into two tracks. Track A fixes the exploration-to-Superpowers workflow and planning contract. Track B preserves the real product architecture in the implementation backlog: plugin-first agent path, reusable skills, deterministic scripts, canonical JSON, separate PDF-generation capability, and future web/API path. The next clean session should implement Track A first while keeping Track B explicitly represented.

**Tech Stack:** Markdown specs and plans, exploration-cycle workflow docs, `small-claims-assistant` plugin docs and assets, Python deterministic scripts, dependency-managed PDF libraries, future BC Gov design-system web path.

---

### Task 1: Consolidate exploration outputs into the Superpowers design baseline

**Files:**
- Modify: `docs/superpowers/specs/2026-06-04-superpowers-host-discovery-design.md`
- Read: `exploration/session-brief.md`
- Read: `exploration/discovery-plans/discovery-plan-2026-06-04.md`
- Read: `exploration/captures/reference-system-findings.md`
- Read: `exploration/captures/plugin-subagent-boundaries.md`
- Read: `exploration/captures/notice-of-claim-canonical-case-json.md`
- Read: `exploration/captures/notice-of-claim-pdf-field-mapping.md`
- Read: `exploration/captures/notice-of-claim-renderer-implementation-checklist.md`

- [ ] **Step 1: Inventory the required upstream exploration artifacts**

Write the upstream input list directly into the design doc so future workers know which exploration artifacts are mandatory inputs before any Superpowers planning begins.

- [ ] **Step 2: Record the full discussed output set**

Expand the design doc so it explicitly includes:

	- plugin-first agent path
	- reusable skills
	- deterministic scripts
	- canonical case JSON
	- separate JSON-to-PDF generation capability
	- future filing-adapter/API boundary
	- future BC Gov design-system web app path
	- workflow and validation outputs required for Superpowers handoff

- [ ] **Step 3: Diagnose execution miss versus source-agent gap**

Add a direct diagnosis section that distinguishes:

	- the session execution failure to carry exploration outputs into the written spec and plan
	- the exploration-cycle source gap where the artifact-to-Superpowers handoff remains too implicit

- [ ] **Step 4: Replace machine-local path examples with repo-relative paths**

Scan the design doc and ensure all repo file references use relative repo paths rather than Windows machine-local absolute paths.

### Task 2: Expand the implementation plan to cover the full output inventory

**Files:**
- Modify: `docs/superpowers/plans/2026-06-04-superpowers-host-discovery-alignment.md`

- [ ] **Step 1: Reframe the plan as a full implementation handoff**

Update the plan header and architecture summary so it covers both workflow correction and product-architecture continuity, not only the host-discovery wording change.

- [ ] **Step 2: Break the work into clean implementation tracks**

Define explicit implementation tracks for:

	- exploration-to-Superpowers workflow fixes
	- exploration-cycle source doc updates
	- current plugin-slice hardening
	- deterministic PDF-generation capability planning
	- product-core backlog preservation
	- clean-session handoff and validation

- [ ] **Step 3: Keep current, next, and deferred outputs visible**

Add task language that separates:

	- what the next clean session should implement now
	- what remains intentionally deferred but still in scope
	- what should remain documented-only until later product slices

- [ ] **Step 4: Remove machine-local absolute paths from the plan**

Rewrite the plan's file references to use repo-relative paths only.

### Task 3: Fix the exploration-cycle source handoff contract

**Files:**
- Modify: `../agent-plugins-skills/plugins/exploration-cycle-plugin/skills/exploration-workflow/SKILL.md`
- Modify: `../agent-plugins-skills/plugins/exploration-cycle-plugin/skills/exploration-workflow/references/phase3-execution-discipline.md`
- Modify: `.agents/skills/exploration-workflow/SKILL.md`
- Modify: `.agents/skills/exploration-workflow/references/phase3-execution-discipline.md`

- [ ] **Step 1: Add an explicit artifact-to-planning rule**

Update the exploration workflow guidance so that when the session is narrowed enough for downstream planning, the planner must inventory the relevant exploration artifacts before writing or revising any Superpowers design or plan.

- [ ] **Step 2: Require task-list rewrites when scope changes**

Strengthen the workflow wording so that if the SME changes output expectations, scope, or execution order, the task ledger must be rewritten before implementation resumes.

- [ ] **Step 3: Preserve the host-aware Superpowers availability rule**

Keep the existing capability-based Superpowers discovery wording in place while adding the stronger handoff contract.

- [ ] **Step 4: Mirror source wording into installed runtime copies**

Apply the same handoff rule in the installed `.agents` copies so local runtime behavior matches the source of truth.

### Task 4: Separate intake-to-JSON from JSON-to-PDF generation

**Files:**
- Review: `plugins/small-claims-assistant/skills/notice-of-claim-intake/SKILL.md`
- Review: `plugins/small-claims-assistant/scripts/write_notice_of_claim_json.py`
- Create: `plugins/small-claims-assistant/skills/notice-of-claim-pdf-generation/SKILL.md`
- Create: `plugins/small-claims-assistant/scripts/render_notice_of_claim_pdf.py`

- [ ] **Step 1: Keep the intake skill scoped to intake and canonical JSON updates**

Do not overload the intake skill with rendering responsibilities. It should gather answers, normalize them, and update canonical JSON.

- [ ] **Step 2: Add a separate deterministic PDF-generation skill**

Create a dedicated generation skill that reads canonical JSON, runs readiness checks, invokes deterministic Python generation code, and returns PDF-generation results.

- [ ] **Step 3: Add a separate renderer entrypoint script**

Create a dedicated renderer script for JSON-to-PDF generation rather than reusing the JSON writer script for rendering concerns.

### Task 5: Add dependency-managed Python support for PDF generation

**Files:**
- Create: `plugins/small-claims-assistant/requirements-core.in`
- Create: `plugins/small-claims-assistant/requirements-core.txt`
- Create: `plugins/small-claims-assistant/requirements-pdf.in`
- Create: `plugins/small-claims-assistant/requirements-pdf.txt`
- Read: `.agent/rules/dependency-management.md`

- [ ] **Step 1: Choose PDF libraries through the dependency rule, not ad hoc installs**

Select the Python PDF/tooling libraries needed for deterministic output and record them in `.in` files first.

- [ ] **Step 2: Compile lockfiles and keep intent plus lock together**

Generate the compiled `.txt` lockfiles from the `.in` files and keep both checked in together.

- [ ] **Step 3: Keep dependency ownership aligned with plugin structure rules**

Make the canonical dependency files live at the plugin root so shared deterministic scripts can use them without duplicating dependency declarations inside each skill folder.

### Task 6: Harden the current `small-claims-assistant` plugin slice

**Files:**
- Review: `plugins/small-claims-assistant/.claude-plugin/plugin.json`
- Review: `plugins/small-claims-assistant/plugin.yaml`
- Review: `plugins/small-claims-assistant/__init__.py`
- Review: `plugins/small-claims-assistant/agents/notice-of-claim-intake-agent.md`
- Review: `plugins/small-claims-assistant/skills/notice-of-claim-intake/SKILL.md`
- Review: `plugins/small-claims-assistant/assets/case-models/notice-of-claim/notice-of-claim-intake-definition.json`
- Review: `plugins/small-claims-assistant/scripts/write_notice_of_claim_json.py`

- [ ] **Step 1: Re-check plugin portability assumptions**

Confirm the active plugin slice does not depend on machine-local paths, stale `.agents` assumptions, or broken relative references.

- [ ] **Step 2: Confirm the current intake slice still matches the explored architecture**

Review the intake agent, skill, and JSON writer against the explored boundaries so the current slice remains aligned with:

	- plugin-first delivery
	- canonical JSON as source of truth
	- deterministic script ownership
	- future split into reusable skills

- [ ] **Step 3: Record any mismatch as follow-on implementation work**

If the current slice is narrower than the final explored architecture, capture that as explicit next-session follow-on work instead of letting it disappear.

### Task 7: Preserve the product backlog that the exploration already defined

**Files:**
- Read: `exploration/captures/plugin-subagent-boundaries.md`
- Read: `exploration/captures/notice-of-claim-canonical-case-json.md`
- Read: `exploration/captures/notice-of-claim-pdf-field-mapping.md`
- Read: `exploration/captures/notice-of-claim-renderer-implementation-checklist.md`

- [ ] **Step 1: Carry the reusable-skill decomposition into the plan**

Keep the following future implementation outputs explicitly present in the plan even if they are not built in the next session:

	- `intake-guidance`
	- `case-normalization`
	- `case-validation`
	- `pdf-generation`
	- `filing-adapter`

- [ ] **Step 2: Carry the deterministic renderer backlog into the plan**

Keep the renderer backlog visible, including:

	- template inventory
	- field binding rules
	- overflow behavior
	- package inclusion rules
	- validation gate before rendering

- [ ] **Step 3: Carry the future web-app and API path into the plan**

Keep the future BC Gov web app and API-backed guidance path visible as deferred outputs that must reuse the same shared legal-output core.

### Task 8: Produce a clean-session implementation entry point

**Files:**
- Modify: `docs/superpowers/plans/2026-06-04-superpowers-host-discovery-alignment.md`

- [ ] **Step 1: Define the exact entry slice for the next clean session**

State clearly that the next implementation session should begin with the exploration-cycle workflow and handoff fixes plus the separate PDF-generation capability planning, not with a fresh round of discovery.

- [ ] **Step 2: Define entry criteria for implementation**

List the artifacts the next session should read first:

	- the updated Superpowers design doc
	- the updated implementation plan
	- the exploration brief and discovery plan
	- the canonical JSON and renderer capture docs
	- the current plugin slice files
	- `.agent/rules/dependency-management.md`

- [ ] **Step 3: Define success criteria for that next session**

Require the next session to finish with:

	- workflow docs updated in canonical and installed copies
	- handoff rules validated
	- separate PDF-generation skill and renderer entrypoint defined or scaffolded
	- dependency files established according to the repo rule
	- no loss of the broader product backlog

### Task 9: Validate the rewritten planning artifacts

**Files:**
- Test: `docs/superpowers/specs/2026-06-04-superpowers-host-discovery-design.md`
- Test: `docs/superpowers/plans/2026-06-04-superpowers-host-discovery-alignment.md`

- [ ] **Step 1: Run targeted file diagnostics**

Use file diagnostics on both rewritten Markdown files and confirm that no file-level errors were introduced.

- [ ] **Step 2: Read back the rewritten sections**

Verify that the design and plan now include:

	- the full explored output set
	- the execution-versus-source diagnosis
	- the exploration artifact inventory
	- repo-relative file references
	- the separate PDF-generation skill and dependency-management slice
	- a clean implementation entry slice for the next session

- [ ] **Step 3: Ask the SME to review the revised spec and plan**

Pause after the rewrite and ask the SME to review the two documents before the next clean implementation session begins.