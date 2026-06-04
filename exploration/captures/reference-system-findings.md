# Reference System Findings

## Scope

These notes capture evidence gathered from the current BC Filing Assistant and its generated PDF package. They are discovery inputs, not a final engineering spec.

## Observed Product Role

- The current Filing Assistant is a structured intake wizard for Small Claims Court forms.
- It is not an AI assistant.
- Its practical job is to collect the information needed to complete official court forms and then output a PDF package.

## Notice Of Claim Flow Observed

The tested path for Notice of Claim required these inputs or decisions:

1. Claimant information
2. Defendant information
3. Claim category
4. Narrative description of what happened
5. Place where the issue arose
6. Date or date range
7. Remedy line items and totals

## PDF Package Structure Observed

The generated output is a package, not a single simple filled page.

Authoritative form source now identified for the main Notice of Claim template:

- Official Form 1 PDF: `https://www2.gov.bc.ca/assets/gov/law-crime-and-justice/courthouse-services/court-files-records/court-forms/small-claims/scl001.pdf`

Observed page types from screenshots:

- Cover page: `NOTICE OF CLAIM`
- Instructional page: `MAKING A CLAIM`
- Main populated Notice of Claim form page
- Attachment page for narrative overflow
- Certificate of Service page

## Layout Implications

- The output must preserve exact form structure rather than produce a custom redesign.
- The official Form 1 PDF should be treated as the source template for the main Notice of Claim form rather than relying only on screenshots from the Filing Assistant package.
- Narrative overflow is handled using a separate attachment-page format.
- Monetary claims are itemized by line, with totals presented in fixed locations.
- Related forms in the same package use their own fixed court layouts.

## Product Implications

- A modern assistant can improve intake and validation without changing the official output contract.
- The right architecture is:
  - guided intake
  - canonical legal data model
  - deterministic court-form PDF renderer
  - optional validation and filing adapters
- The target product now has two intended delivery paths in a standalone repo, but they should not be treated as equal first-slice investments:
  - an interactive AI-native plugin/skill path as the primary initial experience
  - a standalone web app as a secondary path with higher operating complexity
- The plugin/skill path should behave like an interactive filing assistant agent: gather the inputs, validate them, explain unclear prompts, ask follow-up questions, and emit one or more outputs.
- This new filing assistant plugin should be treated as its own standalone product, not as part of `agent-plugins-skills`, even though that ecosystem provides useful reference patterns.
- The plugin-first approach is operationally attractive because clarification help can run inside the user's own AI environment instead of requiring province-hosted model calls.
- A skill can pair AI-guided intake with deterministic local scripts, likely Python-based, to generate the final PDF package after answers are collected and validated.
- Those plugin skills and sub-agents should also be viewed as the prototype for any later hosted AI support in a web app, so the conversational guidance layer can be reused instead of reimplemented.
- If the web app path is pursued, the visual and component direction should follow the BC Government design system rather than an independent design language.
- A shared BC Gov design reference repo is available locally under `temp/repos/claude-design-bc-gov-design-system`, including token CSS, BC Sans fonts, previews, and UI kit material that can accelerate design alignment.
- Current candidate outputs are:
  - exact Notice of Claim PDF package
  - optional mock or future direct e-filing API output
  - canonical case JSON as the normalized structured output shared across rendering and future integrations
- CEIS integration should remain a separate downstream concern until a supported interface is confirmed.

## Current Scope Decision

- First form scope is Notice of Claim only.
- Related forms such as Certificate of Service remain reference evidence for future package expansion, but are not the first implementation slice.

## Known Non-Negotiable

The target system must produce the official BC court forms in exact format, not an approximation.