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

Observed page types from screenshots:

- Cover page: `NOTICE OF CLAIM`
- Instructional page: `MAKING A CLAIM`
- Main populated Notice of Claim form page
- Attachment page for narrative overflow
- Certificate of Service page

## Layout Implications

- The output must preserve exact form structure rather than produce a custom redesign.
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
- The target product now has two intended delivery paths in a standalone repo:
  - a standalone web app
  - an interactive AI-native plugin/skill path
- The plugin/skill path should behave like an interactive filing assistant agent: gather the inputs, validate them, and emit one or more outputs.
- This new filing assistant plugin should be treated as its own standalone product, not as part of `agent-plugins-skills`, even though that ecosystem provides useful reference patterns.
- Current candidate outputs are:
  - exact Notice of Claim PDF package
  - optional mock or future direct e-filing API output
  - [UNCONFIRMED] a third structured output such as canonical case JSON or filing payload package
- CEIS integration should remain a separate downstream concern until a supported interface is confirmed.

## Current Scope Decision

- First form scope is Notice of Claim only.
- Related forms such as Certificate of Service remain reference evidence for future package expansion, but are not the first implementation slice.

## Known Non-Negotiable

The target system must produce the official BC court forms in exact format, not an approximation.