# Notice Of Claim Canonical Case JSON

## Purpose

This document defines the canonical machine-readable case object for the first implementation slice: BC Small Claims Notice of Claim.

This JSON is intended to be the shared contract between:

- guided intake skills and sub-agents
- deterministic PDF generation scripts
- validation and completeness checks
- future mock or live filing adapters
- any later API-backed web application path

The JSON is the source of truth for case data. Host-specific UI state should not be embedded in it.

## Design Principles

- Keep legal case data separate from host-specific conversation state.
- Normalize data into reusable business objects instead of page-by-page PDF fields.
- Preserve enough structure for deterministic rendering, validation, and future filing payload transformation.
- Allow incomplete draft values during intake, but mark their state explicitly.
- Keep the schema reusable across plugin and future web-hosted AI paths.

## Top-Level Shape

```json
{
  "schemaVersion": "1.0.0",
  "formType": "bc-small-claims-notice-of-claim",
  "jurisdiction": {
    "country": "CA",
    "province": "BC",
    "court": "Small Claims Court"
  },
  "caseMetadata": {},
  "claimants": [],
  "defendants": [],
  "claim": {},
  "remedies": [],
  "attachments": [],
  "service": {},
  "validation": {},
  "generation": {}
}
```

## Field Contract

### `schemaVersion`

- Semantic version for the case contract.
- Used to protect renderers and adapters from incompatible changes.

### `formType`

- Fixed string for this first slice.
- Current value: `bc-small-claims-notice-of-claim`

### `jurisdiction`

Basic routing context for rendering and downstream integration.

```json
{
  "country": "CA",
  "province": "BC",
  "court": "Small Claims Court",
  "registryLocation": "Vancouver"
}
```

### `caseMetadata`

Non-substantive metadata about the working draft.

```json
{
  "draftId": "noc-2026-0001",
  "createdAt": "2026-06-04T19:00:00Z",
  "updatedAt": "2026-06-04T19:30:00Z",
  "status": "draft",
  "intakeChannel": "plugin",
  "language": "en"
}
```

Suggested `status` values:

- `draft`
- `ready-for-review`
- `ready-for-pdf`
- `generated`

### `claimants`

Array because a claim may involve more than one claimant.

```json
[
  {
    "id": "claimant-1",
    "type": "individual",
    "name": {
      "full": "Jane Example"
    },
    "contact": {
      "addressLines": ["123 Main Street"],
      "city": "Vancouver",
      "province": "BC",
      "postalCode": "V6B 1A1",
      "phone": "604-555-0101",
      "email": "jane@example.com"
    }
  }
]
```

Suggested `type` values:

- `individual`
- `business`
- `organization`

### `defendants`

Same structure as `claimants`, with optional business-role detail.

```json
[
  {
    "id": "defendant-1",
    "type": "business",
    "name": {
      "full": "ABC Renovations Ltd."
    },
    "contact": {
      "addressLines": ["456 Industrial Way"],
      "city": "Burnaby",
      "province": "BC",
      "postalCode": "V5C 2B2"
    }
  }
]
```

### `claim`

Core factual and venue narrative.

```json
{
  "category": "goods-or-services",
  "summary": "Renovation work was paid for but not completed.",
  "facts": "The defendant agreed to complete kitchen renovation work by March 15, 2026. Payment was made in full, but the work remained incomplete and defective.",
  "location": {
    "city": "Vancouver",
    "province": "BC",
    "country": "CA"
  },
  "incidentDate": {
    "type": "range",
    "start": "2026-02-01",
    "end": "2026-03-15"
  }
}
```

Suggested `category` values should remain controlled and mapped from the intake flow.

### `remedies`

Line-item financial and non-financial outcomes sought.

```json
[
  {
    "id": "remedy-1",
    "type": "money",
    "description": "Refund for incomplete renovation work",
    "amount": {
      "currency": "CAD",
      "value": 3500.0
    }
  }
]
```

Suggested `type` values:

- `money`
- `return-of-property`
- `other-order`

### `attachments`

Logical overflow or supplemental narrative objects, not raw files.

```json
[
  {
    "id": "attachment-1",
    "kind": "facts-overflow",
    "content": "Additional facts that did not fit in the main form body."
  }
]
```

### `service`

Reserved for package continuity and future related-form expansion.

```json
{
  "certificateRequired": true,
  "notes": "Reference-only in first slice; not independently authored yet."
}
```

### `validation`

Machine-readable validation state, separate from user-facing prose.

```json
{
  "isComplete": false,
  "missingFields": ["defendants[0].contact.addressLines"],
  "warnings": [
    {
      "code": "FACTS_TOO_VAGUE",
      "message": "The narrative may need more specific dates or actions."
    }
  ]
}
```

### `generation`

Output bookkeeping for deterministic generation.

```json
{
  "pdf": {
    "ready": false,
    "templateVersion": "bc-scc-form1-v1"
  },
  "filingPayload": {
    "ready": false
  }
}
```

## What Does Not Belong In This JSON

- raw LLM prompt history
- host-specific thread IDs or session IDs that are irrelevant outside the current runtime
- UI widget state
- rendering coordinates tied directly to PDF field placement
- provider-specific token or billing metadata

## Host-Agnostic Rules

- The plugin path may collect data conversationally, but it should emit this JSON contract.
- A future web app API path should also emit and consume the same contract.
- The PDF renderer should read this JSON and map it deterministically to official forms.
- Filing adapters should transform this JSON into downstream payloads rather than bypassing it.

## Open Contract Questions

- Exact controlled vocabulary for claim categories
- Exact support model for multiple claimants or defendants in the first slice
- Whether `service` should remain reserved or be expanded now to support full package generation logic
- Whether machine-readable validation codes should be standardized in a separate reference file