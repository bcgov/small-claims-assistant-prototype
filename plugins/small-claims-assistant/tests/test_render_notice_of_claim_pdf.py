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

from pypdf import PdfReader


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PLUGIN_ROOT / "scripts" / "render_notice_of_claim_pdf.py"


class RenderNoticeOfClaimPdfTest(unittest.TestCase):
    """Verify the deterministic renderer CLI contract."""

    def extract_pdf_text(self, pdf_path: Path) -> str:
        """Return normalized text extracted from the generated PDF."""

        reader = PdfReader(str(pdf_path))
        return "\n".join((page.extract_text() or "") for page in reader.pages)

    def extract_pdf_page_text(self, pdf_path: Path, page_number: int) -> str:
        """Return extracted text for one 1-based PDF page."""

        reader = PdfReader(str(pdf_path))
        return reader.pages[page_number - 1].extract_text() or ""

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
        """A ready case should produce a PDF containing the case facts and parties."""

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

            pdf_text = self.extract_pdf_text(package_path)
            self.assertIn("Jane Example", pdf_text)
            self.assertIn("ABC Renovations Ltd.", pdf_text)
            self.assertIn("The defendant agreed to complete kitchen renovation work by March 15, 2026.", pdf_text)
            self.assertIn("3500", pdf_text)

            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["status"], "generated")
            self.assertEqual(manifest["templateVersion"], "bc-scc-form1-v1")
            self.assertEqual(manifest["artifacts"][0]["kind"], "package-pdf")
            self.assertEqual(manifest["artifacts"][0]["path"], str(package_path))

    def test_does_not_repeat_summary_inside_main_narrative(self) -> None:
        """The form narrative should not duplicate the claim summary when facts already cover it."""

        payload = self.build_case_payload(is_complete=True)
        payload["claim"]["summary"] = "Jane Example paid ABC Renovations Ltd. for work that was not completed."
        payload["claim"]["facts"] = (
            "Jane Example paid ABC Renovations Ltd. for work that was not completed. "
            "The defendant promised to finish the renovation by March 15, 2026 but failed to do so."
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            input_path = temp_path / "case.json"
            output_dir = temp_path / "output"
            input_path.write_text(json.dumps(payload), encoding="utf-8")

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
            page_text = self.extract_pdf_page_text(package_path, 3)
            repeated_clause = "for work that was not completed."

            self.assertEqual(page_text.count(repeated_clause), 1)

    def test_populates_only_the_notice_of_claim_page(self) -> None:
        """The rendered draft should place claim data on page 3 (Notice of Claim form) only."""

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

            reader = PdfReader(str(package_path))
            self.assertEqual(len(reader.pages), 4, "Output must match the 4-page official template.")

            notice_page = self.extract_pdf_page_text(package_path, 3)
            certificate_page = self.extract_pdf_page_text(package_path, 4)

            self.assertIn("Jane Example", notice_page)
            self.assertNotIn("Jane Example", certificate_page)


if __name__ == "__main__":
    unittest.main()