# Purpose: Transform canonical Notice of Claim JSON into deterministic mock filing-adapter artifacts.

"""Deterministic mock API adapter for Notice of Claim submissions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


# Keep the adapter contract host-agnostic and driven only by canonical JSON.
def load_case_payload(input_path: Path) -> dict[str, Any]:
    """Read the canonical case JSON from disk."""

    return json.loads(input_path.read_text(encoding="utf-8"))


# Keep filing readiness independent from the renderer while using the same source of truth.
def validate_ready_for_filing(case_data: dict[str, Any]) -> None:
    """Reject canonical case drafts that are not yet ready for filing-payload generation."""

    validation = case_data.get("validation", {})
    generation = case_data.get("generation", {}).get("filingPayload", {})
    case_status = case_data.get("caseMetadata", {}).get("status")

    if not validation.get("isComplete"):
        raise ValueError("Case is not ready for filing payload generation: validation.isComplete must be true.")

    if not generation.get("ready"):
        raise ValueError("Case is not ready for filing payload generation: generation.filingPayload.ready must be true.")

    if case_status not in {"ready-for-review", "generated"}:
        raise ValueError("Case is not ready for filing payload generation: caseMetadata.status must be ready-for-review or generated.")


# Emit a stable mock payload shape so later integrations and hosts can depend on one seam.
def build_mock_request(case_data: dict[str, Any]) -> dict[str, Any]:
    """Build the deterministic mock filing request payload."""

    first_claimant = case_data.get("claimants", [{}])[0]
    first_defendant = case_data.get("defendants", [{}])[0]
    first_remedy = case_data.get("remedies", [{}])[0]

    return {
        "caseId": case_data.get("caseMetadata", {}).get("draftId"),
        "formType": case_data.get("formType"),
        "submissionChannel": "plugin-mock-api",
        "registryLocation": case_data.get("jurisdiction", {}).get("registryLocation"),
        "claimant": {
            "name": first_claimant.get("name", {}).get("full"),
            "email": first_claimant.get("contact", {}).get("email"),
        },
        "defendant": {
            "name": first_defendant.get("name", {}).get("full"),
        },
        "claimSummary": case_data.get("claim", {}).get("summary"),
        "claimAmount": first_remedy.get("amount", {}),
    }


# Store adapter artifacts explicitly so a later real API boundary can keep the same contract.
def write_json(output_path: Path, payload: dict[str, Any]) -> Path:
    """Write a JSON artifact to disk."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return output_path


# The mock response represents the future downstream adapter boundary without external side effects.
def build_mock_response(request_path: Path, request_payload: dict[str, Any]) -> dict[str, Any]:
    """Build a deterministic mock API response for the request artifact."""

    return {
        "status": "accepted",
        "submissionId": f"mock-{request_payload['caseId']}",
        "requestPath": str(request_path),
        "message": "Mock filing adapter accepted the Notice of Claim payload.",
    }


# Keep the CLI narrow so skills and later hosts can reuse one stable submission entrypoint.
def main() -> int:
    """Validate canonical JSON and emit deterministic mock submission artifacts."""

    parser = argparse.ArgumentParser(
        description="Submit a BC Notice of Claim canonical JSON payload to the deterministic mock filing adapter."
    )
    parser.add_argument("--input", required=True, help="Path to the canonical case JSON file.")
    parser.add_argument("--output-dir", required=True, help="Directory for the mock request and response artifacts.")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)

    try:
        case_data = load_case_payload(input_path)
        validate_ready_for_filing(case_data)
        request_payload = build_mock_request(case_data)
        request_path = write_json(output_dir / "mock-filing-request.json", request_payload)
        response_payload = build_mock_response(request_path, request_payload)
        write_json(output_dir / "mock-filing-response.json", response_payload)
    except Exception as exc:  # pragma: no cover - exercised via subprocess tests.
        print(str(exc), file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())