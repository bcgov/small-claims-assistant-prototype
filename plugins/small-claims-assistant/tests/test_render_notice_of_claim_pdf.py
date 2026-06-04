# Purpose: Lock the first deterministic Notice of Claim renderer contract before implementation.

"""Contract tests for the Notice of Claim PDF renderer entrypoint."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PLUGIN_ROOT / "scripts" / "render_notice_of_claim_pdf.py"


class RenderNoticeOfClaimPdfTest(unittest.TestCase):
    """Verify the deterministic renderer CLI contract."""

    def build_case_payload(self, *, is_complete: bool) -> dict[str, Any]:
        """Return the smallest canonical JSON payload needed for renderer tests."""

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
                "draftId": "noc-test-001",
                "status": "ready-for-pdf" if is_complete else "draft",
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
                "isComplete": is_complete,
                "missingFields": [] if is_complete else ["validation.isComplete"],
                "warnings": [],
            },
            "generation": {
                "pdf": {"ready": is_complete, "templateVersion": "bc-scc-form1-v1"},
                "filingPayload": {"ready": False},
            },
        }

    def run_renderer(self, *, payload: dict[str, Any]) -> subprocess.CompletedProcess[str]:
        """Execute the renderer CLI against a temporary JSON payload."""

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

    def test_rejects_case_not_ready_for_pdf(self) -> None:
        """The renderer must refuse incomplete canonical JSON."""

        result = self.run_renderer(payload=self.build_case_payload(is_complete=False))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not ready for PDF generation", result.stderr)

    def test_writes_pdf_package_and_manifest_for_ready_case(self) -> None:
        """A ready case should produce a deterministic PDF artifact manifest."""

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            input_path = temp_path / "case.json"
            output_dir = temp_path / "output"
            input_path.write_text(
                json.dumps(self.build_case_payload(is_complete=True)),
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

            package_path = output_dir / "notice-of-claim-package.pdf"
            manifest_path = output_dir / "render-manifest.json"

            self.assertTrue(package_path.exists())
            self.assertTrue(manifest_path.exists())

            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["status"], "generated")
            self.assertEqual(manifest["templateVersion"], "bc-scc-form1-v1")
            self.assertEqual(manifest["artifacts"][0]["kind"], "package-pdf")
            self.assertEqual(manifest["artifacts"][0]["path"], str(package_path))


if __name__ == "__main__":
    unittest.main()