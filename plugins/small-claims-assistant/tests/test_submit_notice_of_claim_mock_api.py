# Purpose: Lock the first deterministic mock filing-adapter contract before implementation.

"""Contract tests for the Notice of Claim mock filing adapter."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PLUGIN_ROOT / "scripts" / "submit_notice_of_claim_mock_api.py"


class SubmitNoticeOfClaimMockApiTest(unittest.TestCase):
    """Verify the deterministic mock filing-adapter CLI contract."""

    def build_case_payload(self, *, ready: bool) -> dict[str, Any]:
        """Return the smallest canonical JSON payload needed for adapter tests."""

        return {
            "schemaVersion": "1.0.0",
            "formType": "bc-small-claims-notice-of-claim",
            "jurisdiction": {
                "country": "CA",
                "province": "BC",
                "court": "Small Claims Court",
                "registryLocation": "Vancouver",
            },
            "caseMetadata": {
                "draftId": "noc-api-001",
                "status": "ready-for-review" if ready else "draft",
                "intakeChannel": "plugin",
                "language": "en",
            },
            "claimants": [
                {
                    "id": "claimant-1",
                    "type": "individual",
                    "name": {"full": "Jane Example"},
                    "contact": {
                        "addressLines": ["123 Main Street"],
                        "city": "Vancouver",
                        "province": "BC",
                        "postalCode": "V6B 1A1",
                        "email": "jane@example.com",
                    },
                }
            ],
            "defendants": [
                {
                    "id": "defendant-1",
                    "type": "business",
                    "name": {"full": "ABC Renovations Ltd."},
                    "contact": {
                        "addressLines": ["456 Industrial Way"],
                        "city": "Burnaby",
                        "province": "BC",
                        "postalCode": "V5C 2B2",
                    },
                }
            ],
            "claim": {
                "category": "goods-or-services",
                "summary": "Renovation work was paid for but not completed.",
                "facts": "The defendant agreed to complete kitchen renovation work by March 15, 2026.",
                "location": {"city": "Vancouver", "province": "BC", "country": "CA"},
                "incidentDate": {"type": "single", "start": "2026-03-15"},
            },
            "remedies": [
                {
                    "id": "remedy-1",
                    "type": "money",
                    "description": "Refund for incomplete renovation work",
                    "amount": {"currency": "CAD", "value": 3500.0},
                }
            ],
            "attachments": [],
            "service": {"certificateRequired": True, "notes": "Reserved for later package expansion."},
            "validation": {
                "isComplete": ready,
                "missingFields": [] if ready else ["validation.isComplete"],
                "warnings": [],
            },
            "generation": {
                "pdf": {"ready": ready, "templateVersion": "bc-scc-form1-v1"},
                "filingPayload": {"ready": ready},
            },
        }

    def run_adapter(self, *, payload: dict[str, Any]) -> subprocess.CompletedProcess[str]:
        """Execute the adapter CLI against a temporary JSON payload."""

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            input_path = temp_path / "case.json"
            output_dir = temp_path / "output"
            input_path.write_text(json.dumps(payload), encoding="utf-8")

            return subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--input",
                    str(input_path),
                    "--output-dir",
                    str(output_dir),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

    def test_rejects_case_not_ready_for_mock_submission(self) -> None:
        """The filing adapter must refuse incomplete canonical JSON."""

        result = self.run_adapter(payload=self.build_case_payload(ready=False))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not ready for filing payload generation", result.stderr)

    def test_writes_request_and_response_artifacts_for_ready_case(self) -> None:
        """A ready case should produce deterministic request and response artifacts."""

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            input_path = temp_path / "case.json"
            output_dir = temp_path / "output"
            input_path.write_text(
                json.dumps(self.build_case_payload(ready=True)),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--input",
                    str(input_path),
                    "--output-dir",
                    str(output_dir),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)

            request_path = output_dir / "mock-filing-request.json"
            response_path = output_dir / "mock-filing-response.json"

            self.assertTrue(request_path.exists())
            self.assertTrue(response_path.exists())

            request_payload = json.loads(request_path.read_text(encoding="utf-8"))
            response_payload = json.loads(response_path.read_text(encoding="utf-8"))

            self.assertEqual(request_payload["caseId"], "noc-api-001")
            self.assertEqual(request_payload["claimAmount"]["value"], 3500.0)
            self.assertEqual(request_payload["submissionChannel"], "plugin-mock-api")
            self.assertEqual(response_payload["status"], "accepted")
            self.assertEqual(response_payload["requestPath"], str(request_path))


if __name__ == "__main__":
    unittest.main()