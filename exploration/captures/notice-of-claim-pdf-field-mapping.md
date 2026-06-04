# Notice Of Claim PDF Field Mapping

## Purpose

This artifact maps the observed BC Small Claims Notice of Claim PDF package back to the canonical case JSON.

It is not the final renderer spec. It is the discovery bridge between:

- the observed Filing Assistant output package
- the canonical Notice of Claim case JSON
- the future deterministic PDF renderer boundary

The main goal is to prevent the implementation from drifting into page-shaped business logic too early.

## Scope

- First slice only: Notice of Claim package
- Based on the observed package pages from the BC Filing Assistant walkthrough
- Uses the canonical JSON defined in `exploration/captures/notice-of-claim-canonical-case-json.md`
- Includes both direct field mappings and renderer-derived behaviors
- The authoritative source template for the main Notice of Claim form is the official BC Form 1 PDF: `https://www2.gov.bc.ca/assets/gov/law-crime-and-justice/courthouse-services/court-files-records/court-forms/small-claims/scl001.pdf`

## Mapping Principles

- Canonical JSON remains the source of truth.
- PDF coordinates, field rectangles, and pagination rules belong in renderer templates, not in the case JSON.
- Some pages in the package are mostly static template output and do not require user-authored JSON fields.
- Overflow handling is a renderer responsibility driven by canonical data length, not a separate user workflow unless the product later chooses to expose it explicitly.
- Fields marked as inferred still need confirmation against the official form package or a more detailed PDF inspection pass.
- Where screenshots and the official Form 1 PDF diverge in clarity, the official Form 1 PDF should win for the main form-page layout.

## Package-Level Mapping

| Package page | Role in package | Primary JSON source | Mapping status |
|---|---|---|---|
| Cover page | Static package cover for Notice of Claim | `formType`, package template metadata | Inferred |
| Making a Claim page | Static instructional page | none or package template metadata | Observed |
| Main Notice of Claim form | Primary court form page | `jurisdiction`, `claimants`, `defendants`, `claim`, `remedies` | Observed |
| Attachment page | Overflow continuation for narrative content | `claim.facts`, `attachments[]` | Observed |
| Certificate of Service page | Related package page | `service` | Observed but first-slice authoring remains partial |

## Page 1: Cover Page

Observed role: package-level title page labeled `NOTICE OF CLAIM`.

### Mapping

| PDF area | Canonical source | Rule | Confidence |
|---|---|---|---|
| Package title | `formType` mapped through renderer template | Renderer chooses the official human-readable title for the package | Medium |
| Versioned template identity | `generation.pdf.templateVersion` | Internal renderer bookkeeping, not user-visible unless needed | Medium |
| Court branding and static labels | none | Template-owned, not driven by case JSON | High |

### Notes

- This page appears to be mostly template-owned.
- The renderer should treat it as static package content with minimal or no claimant-entered data.

## Page 2: Making A Claim Instructional Page

Observed role: instructional court page included in the package.

### Mapping

| PDF area | Canonical source | Rule | Confidence |
|---|---|---|---|
| Instructional body text | none | Static page shipped with the package template | High |
| Court/static headings | none | Template-owned | High |

### Notes

- No case-specific JSON fields should be designed just to support this page.
- The renderer should include this page when producing the official package if the official package requires it.

## Page 3: Main Notice Of Claim Form

Observed role: the primary filled court form page.

### Registry and court context

| PDF field/area | Canonical source | Rule | Confidence |
|---|---|---|---|
| Court name / form jurisdiction | `jurisdiction.court` | Render official court label or template variant | Medium |
| Registry location | `jurisdiction.registryLocation` | Populate the registry field if the official form requires it | Medium |

### Claimant section

| PDF field/area | Canonical source | Rule | Confidence |
|---|---|---|---|
| Claimant name block | `claimants[].name.full` | Render in form order; first slice may limit layout if many parties | High |
| Claimant address block | `claimants[].contact.addressLines`, `city`, `province`, `postalCode` | Flatten into court form mailing-address format | High |
| Claimant contact details | `claimants[].contact.phone`, `email` | Populate only if the official form has fields for them | Medium |

### Defendant section

| PDF field/area | Canonical source | Rule | Confidence |
|---|---|---|---|
| Defendant name block | `defendants[].name.full` | Render in form order | High |
| Defendant address block | `defendants[].contact.addressLines`, `city`, `province`, `postalCode` | Flatten into court form mailing-address format | High |
| Defendant type distinctions | `defendants[].type` | May affect label formatting for business or organization names, but not the canonical data shape | Medium |

### Claim classification and factual narrative

| PDF field/area | Canonical source | Rule | Confidence |
|---|---|---|---|
| Claim category / checkbox selection | `claim.category` | Map controlled value to official form checkbox or category wording | Medium |
| Short claim summary | `claim.summary` | Use where the form expects a concise statement, if distinct from full facts | Medium |
| Main factual narrative | `claim.facts` | Fill the main narrative area until the page limit is reached | High |

### Location and date section

| PDF field/area | Canonical source | Rule | Confidence |
|---|---|---|---|
| Place where issue arose | `claim.location.city`, `province`, `country` | Render in the court form's expected location text format | High |
| Single incident date | `claim.incidentDate.start` | Used when `claim.incidentDate.type = single` | Medium |
| Date range | `claim.incidentDate.start`, `claim.incidentDate.end` | Used when `claim.incidentDate.type = range` | Medium |

### Remedy and monetary section

| PDF field/area | Canonical source | Rule | Confidence |
|---|---|---|---|
| Remedy line description | `remedies[].description` | Render each line item in order | High |
| Remedy amount | `remedies[].amount.value`, `currency` | Format in CAD and place in fixed amount locations | High |
| Remedy type distinctions | `remedies[].type` | May drive whether a line is monetary or non-monetary and whether a value is shown | Medium |
| Total amount claimed | derived from `remedies[]` | Sum monetary line items in renderer, do not store duplicate total unless required for interoperability | High |

## Page 4: Attachment Page For Overflow

Observed role: continuation page for claim narrative overflow.

### Mapping

| PDF field/area | Canonical source | Rule | Confidence |
|---|---|---|---|
| Overflow narrative body | `claim.facts` | Renderer continues remaining narrative text when the main form body overflows | High |
| Explicit supplemental narrative | `attachments[]` where `kind = facts-overflow` | Optional explicit support if the product later stores overflow as a logical attachment object | Medium |
| Page continuation label | none | Template-owned, controlled by renderer | High |
| Party/case carry-forward context | `claimants[]`, `defendants[]`, maybe `caseMetadata.draftId` | Include only if the official attachment format requires contextual headers | Low |

### Notes

- The preferred first-slice model is to treat overflow as a renderer behavior from `claim.facts`.
- `attachments[]` should remain available for explicit continuation objects or future supporting material, but the renderer should not require a separate attachment object just to continue long facts text.

## Page 5: Certificate Of Service Page

Observed role: related court page included in the package.

### Mapping

| PDF field/area | Canonical source | Rule | Confidence |
|---|---|---|---|
| Include certificate page in package | `service.certificateRequired` | Renderer may include the official certificate page when producing the package | Medium |
| Service notes / reserved continuity | `service.notes` | Reserved for future expansion; not enough evidence yet for full authoring contract | Medium |
| Service-specific factual fields | future `service.*` expansion | Do not invent detailed fields until the package is inspected more closely | High |

### Notes

- The package evidence shows this page exists, but the current first-slice product scope is still Notice of Claim only.
- For now, treat `service` as a reserved continuity object rather than a fully modeled intake section.

## Renderer-Derived Behaviors

These behaviors are required even though they do not map one-to-one to a single canonical field.

| Behavior | Canonical inputs | Rule |
|---|---|---|
| Party ordering | `claimants[]`, `defendants[]` | Preserve intake order unless a court-specific ordering rule is later defined |
| Address flattening | party contact objects | Convert structured address parts into the official line layout expected by the form |
| Narrative truncation and continuation | `claim.facts` | Fill main form text area first, then continue on attachment page |
| Money total calculation | `remedies[]` | Sum monetary remedies in renderer logic |
| Conditional page inclusion | package template + `service.*` + overflow state | Include static or related pages based on official package requirements |
| Controlled vocabulary rendering | `claim.category`, `remedies[].type` | Map internal controlled values to official labels or checkbox states |

## Canonical JSON Coverage Summary

| Canonical section | PDF usage in first slice |
|---|---|
| `schemaVersion` | compatibility and renderer routing only |
| `formType` | package template selection |
| `jurisdiction` | court and registry context |
| `caseMetadata` | operational metadata; mostly non-visible in PDF |
| `claimants` | main form claimant block |
| `defendants` | main form defendant block |
| `claim` | classification, facts, location, date |
| `remedies` | line items and totals |
| `attachments` | optional logical support for explicit overflow or future supplements |
| `service` | reserved continuity for package-related future work |
| `validation` | not rendered directly; used to gate PDF generation |
| `generation` | internal renderer bookkeeping |

## First-Slice Decisions Anchored By This Mapping

- The renderer should be built around the canonical case JSON, not around host conversation state.
- Static package pages should remain template-owned and should not cause schema bloat.
- Narrative overflow should be implemented as deterministic renderer continuation logic.
- The `service` object should remain reserved until a more detailed inspection of the Certificate of Service page is completed.
- Totals and layout behaviors should be derived in the renderer instead of duplicated into canonical storage.

## Open Questions For The Next Inspection Pass

1. What exact claim-category values appear on the official Notice of Claim form and how should they map from `claim.category`?
2. What exact line-item structure and labels are used on the remedy section of the official form?
3. Does the main form surface phone and email fields for parties, or only mailing address data?
4. What exact headers or carry-forward fields appear on the attachment page?
5. Which fields on the Certificate of Service page should be modeled now versus deferred?
6. Does the package require any hidden identifiers, filing codes, or registry metadata beyond the currently proposed `jurisdiction.registryLocation`?
7. Which package pages come directly from the official Form 1 template versus being assembled as companion pages by the Filing Assistant package flow?

## Recommended Immediate Follow-On

The next artifact should convert this page-and-field mapping into a renderer-facing implementation checklist:

- required template pages
- direct field bindings
- derived calculations
- overflow rules
- page inclusion conditions
- unresolved evidence gaps