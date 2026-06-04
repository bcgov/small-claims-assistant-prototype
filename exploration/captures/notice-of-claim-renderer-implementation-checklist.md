# Notice Of Claim Renderer Implementation Checklist

## Purpose

This checklist converts the discovery mapping into an implementation-facing worklist for the first deterministic PDF renderer slice.

It is intended to guide the first plugin-first build without collapsing the canonical case model into page-specific host logic.

## Inputs This Checklist Depends On

- `exploration/captures/notice-of-claim-canonical-case-json.md`
- `exploration/captures/notice-of-claim-pdf-field-mapping.md`
- `exploration/captures/plugin-subagent-boundaries.md`
- `exploration/captures/reference-system-findings.md`

## First-Slice Build Target

Build one deterministic renderer that:

- accepts canonical Notice of Claim case JSON
- validates readiness for generation
- renders the observed Notice of Claim package shape
- handles narrative overflow deterministically
- keeps package-template concerns separate from intake and AI guidance

## Plugin Packaging Assumptions

The eventual plugin implementation should follow the repo's plugin structure rules:

- shared renderer code and template assets should live once under the plugin root
- the plugin root should own shared `assets/`, `scripts/`, and `references/`
- skill folders should expose needed `assets/`, `scripts/`, and `references/` entries via file-level symlinks
- no directory symlinks
- no duplicated renderer scripts across skills

This means the first implementation should be designed as a shared plugin-level renderer capability that a generation skill can invoke, not as a one-off script copied into multiple skills.

## Checklist

## 1. Renderer Boundary

- [ ] Define the renderer entrypoint contract: input JSON file or object, output package path or artifact manifest.
- [ ] Keep the renderer free of host conversation state, prompt history, or plugin runtime thread identifiers.
- [ ] Decide whether the first implementation outputs a single combined PDF package or a deterministic folder of package pages before bundling.
- [ ] Define failure behavior when `validation.isComplete = false`.

## 2. Template Inventory

- [ ] Inventory the exact template pages required for the first package:
  - cover page
  - `Making a Claim` page
  - main Notice of Claim form page
  - attachment overflow page
  - Certificate of Service page, if included in first-slice package generation
- [ ] Identify which pages are static-template pages versus data-bound pages.
- [ ] Identify where the official form files or reconstruction assets will live in the plugin structure.
- [ ] Record template versioning strategy under `generation.pdf.templateVersion`.

## 3. Direct Field Bindings

### Court and registry

- [ ] Bind `jurisdiction.court` to the form's court label logic.
- [ ] Bind `jurisdiction.registryLocation` to any required registry field.

### Claimants

- [ ] Bind claimant full names from `claimants[].name.full`.
- [ ] Bind claimant address lines from `claimants[].contact.*`.
- [ ] Confirm whether phone and email appear on the official form before binding them.

### Defendants

- [ ] Bind defendant full names from `defendants[].name.full`.
- [ ] Bind defendant address lines from `defendants[].contact.*`.
- [ ] Confirm whether defendant `type` changes labeling or only business rules.

### Claim facts

- [ ] Bind `claim.category` to official checkbox or label behavior.
- [ ] Bind `claim.summary` only if the official form exposes a separate short summary field.
- [ ] Bind `claim.facts` to the main narrative region.
- [ ] Bind `claim.location.*` to the place-of-dispute area.
- [ ] Bind `claim.incidentDate.*` to either single-date or date-range presentation.

### Remedies

- [ ] Bind remedy descriptions from `remedies[].description`.
- [ ] Bind money values from `remedies[].amount.value`.
- [ ] Confirm how non-monetary remedy types should appear on the form.

## 4. Derived Calculations

- [ ] Calculate total monetary claim from `remedies[]` in renderer logic.
- [ ] Flatten structured addresses into court-form line formatting.
- [ ] Determine whether party ordering is simply intake order or whether the court form imposes another order.
- [ ] Map controlled vocabulary values into official printed labels without storing duplicate print strings in canonical JSON.

## 5. Overflow Rules

- [ ] Define the maximum narrative capacity of the main Notice of Claim form page.
- [ ] Continue overflow text onto the attachment page deterministically.
- [ ] Keep overflow generation driven primarily by `claim.facts`, not by requiring hand-authored attachment objects.
- [ ] Decide whether `attachments[]` is supported in the first renderer or deferred to a later slice.
- [ ] Define page-break behavior for long text so the same input always yields the same output.

## 6. Package Inclusion Rules

- [ ] Confirm whether the cover page is always included.
- [ ] Confirm whether the instructional `Making a Claim` page is always included.
- [ ] Confirm whether the Certificate of Service page is included in the first generated package or deferred.
- [ ] Define whether attachment pages are included only when overflow exists.

## 7. Validation Gate Before Render

- [ ] Define the minimum required fields for `ready-for-pdf`.
- [ ] Turn validation warnings versus blocking errors into deterministic generation rules.
- [ ] Decide whether the renderer should refuse incomplete inputs or generate a flagged draft output.
- [ ] Align this gate with the `validation` object in canonical JSON rather than creating a second readiness model.

## 8. Output Contract

- [ ] Define where the renderer writes generated artifacts.
- [ ] Define whether `generation.pdf.ready` is set before or after successful artifact creation.
- [ ] Define a machine-readable generation result object or manifest.
- [ ] Decide whether the first slice also emits a filing-payload placeholder alongside the PDF.

## 9. Evidence Gaps To Resolve

- [ ] Confirm the exact official claim-category options shown on the Notice of Claim form.
- [ ] Confirm the exact remedy-section layout and line-item labels.
- [ ] Confirm which claimant and defendant contact fields truly appear on the printed form.
- [ ] Confirm attachment-page header requirements.
- [ ] Confirm how much of the Certificate of Service page should be modeled now.
- [ ] Confirm any hidden or implied package metadata required by the official form set.

## 10. Suggested Build Order

- [ ] Step 1: load and validate canonical JSON.
- [ ] Step 2: render the main Notice of Claim form page with direct bindings only.
- [ ] Step 3: add remedy totals and date/location formatting.
- [ ] Step 4: add overflow continuation page logic.
- [ ] Step 5: add static package pages.
- [ ] Step 6: decide on Certificate of Service inclusion for first slice.
- [ ] Step 7: emit deterministic artifact manifest and generation metadata.

## Recommended Immediate Follow-On After This Checklist

The next artifact should be a renderer-facing requirement spec or task breakdown that names:

- the first renderer module
- the expected template asset locations
- validation responsibilities
- package assembly responsibilities
- open questions that must be closed before coding