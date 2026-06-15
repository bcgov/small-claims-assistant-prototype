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
# FROM-section claimant name must land here (below NAME label y=680, above Form38 checkbox y=669).
CLAIMANT_NAME_Y_MIN, CLAIMANT_NAME_Y_MAX = 660.0, 685.0
# FROM section top — address lines must NOT appear above this threshold.
FROM_SECTION_CLAIMANT_ONLY_THRESHOLD = 620.0
# TO-section defendant name must land below the NAME label (y=616).
DEFENDANT_NAME_Y_MIN, DEFENDANT_NAME_Y_MAX = 595.0, 625.0
# WHERE city must land near the CITY/TOWN/MUNICIPALITY labels (y=449/443).
WHERE_CITY_Y_MIN, WHERE_CITY_Y_MAX = 425.0, 455.0
# WHEN date must land in the WHEN column (annotation rect y=400–440).
WHEN_DATE_Y_MIN, WHEN_DATE_Y_MAX = 405.0, 445.0
# First remedy row (a) must land near the 'a' label (y=386.9) and its $ (y=376.4).
REMEDY_ROW_A_Y_MIN, REMEDY_ROW_A_Y_MAX = 360.0, 395.0
# Sub-total must land at the TOTAL row (y=226.8 / $ y=225.5).
TOTAL_Y_MIN, TOTAL_Y_MAX = 215.0, 235.0
# WHAT HAPPENED section y-bounds (below the WHAT HAPPENED? label at y≈527, above WHERE at y≈440).
FACTS_Y_MIN, FACTS_Y_MAX = 445.0, 510.0
# TO section prov/postal row: postal code must be to the right of the city column.
TO_POSTAL_X_MIN = 250.0
# WHEN date x must be inside the leftWhen annotation box (rect x=322..402.9).
WHEN_DATE_X_MAX = 410.0
SCRIPT_PATH = PLUGIN_ROOT / "scripts" / "render_notice_of_claim_pdf.py"


class RenderNoticeOfClaimPdfTest(unittest.TestCase):
    """Verify the deterministic renderer CLI contract."""

    def extract_pdf_text(self, pdf_path: Path) -> str:
        """Return normalized text extracted from the generated PDF."""

        reader = PdfReader(str(pdf_path))
        return "\n".join((page.extract_text() or "") for page in reader.pages)

    def extract_page_text_positions(self, pdf_path: Path, page_number: int) -> list[tuple[float, float, str]]:
        """Return (y, x, text) tuples for every non-blank text run on a page."""

        reader = PdfReader(str(pdf_path))
        page = reader.pages[page_number - 1]
        parts: list[tuple[float, float, str]] = []

        def _visitor(text: str, cm: Any, tm: Any, fontDict: Any, fontSize: Any) -> None:
            if text and text.strip():
                parts.append((round(tm[5], 1), round(tm[4], 1), text.strip()))

        page.extract_text(visitor_text=_visitor)
        return parts

    def find_y_for_text(self, positions: list[tuple[float, float, str]], needle: str) -> float | None:
        """Return the y-coordinate of the first text fragment that contains needle."""

        for y, _x, text in positions:
            if needle in text:
                return y
        return None

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

    # ------------------------------------------------------------------
    # Position-aware layout tests — these reproduce the coordinate bugs.
    # ------------------------------------------------------------------

    def _render_to_tmpdir(self, payload: dict[str, Any]) -> Path:
        """Render payload to a temp dir and return the package PDF path."""

        temp_dir = tempfile.mkdtemp()
        temp_path = Path(temp_dir)
        input_path = temp_path / "case.json"
        output_dir = temp_path / "output"
        input_path.write_text(json.dumps(payload), encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "--input", str(input_path), "--output-dir", str(output_dir)],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        return output_dir / "notice-of-claim-package.pdf"

    def test_claimant_name_placed_in_from_section(self) -> None:
        """Claimant name must land in the FROM section (y between 660 and 685)."""

        pdf_path = self._render_to_tmpdir(self.build_case_payload(is_complete=True))
        positions = self.extract_page_text_positions(pdf_path, 3)
        y = self.find_y_for_text(positions, "Jane Example")
        self.assertIsNotNone(y, "Claimant name not found on notice page")
        self.assertGreaterEqual(y, CLAIMANT_NAME_Y_MIN, f"Claimant name too low: y={y}")
        self.assertLessEqual(y, CLAIMANT_NAME_Y_MAX, f"Claimant name too high: y={y}")

    def test_claimant_address_not_in_from_section(self) -> None:
        """FROM section (y > 620) must contain only the claimant name, not the full address."""

        pdf_path = self._render_to_tmpdir(self.build_case_payload(is_complete=True))
        positions = self.extract_page_text_positions(pdf_path, 3)
        in_from = [(y, x, t) for y, x, t in positions if y > FROM_SECTION_CLAIMANT_ONLY_THRESHOLD and x > 100]
        texts_in_from = {t for _y, _x, t in in_from}
        self.assertNotIn("123 Main Street", texts_in_from, "Claimant street address must not appear in FROM section")
        self.assertNotIn("V6B 1A1", " ".join(texts_in_from), "Claimant postal code must not appear in FROM section")

    def test_defendant_name_placed_in_to_section(self) -> None:
        """Defendant name must land in the TO section (y between 595 and 625)."""

        pdf_path = self._render_to_tmpdir(self.build_case_payload(is_complete=True))
        positions = self.extract_page_text_positions(pdf_path, 3)
        y = self.find_y_for_text(positions, "ABC Renovations Ltd.")
        self.assertIsNotNone(y, "Defendant name not found on notice page")
        self.assertGreaterEqual(y, DEFENDANT_NAME_Y_MIN, f"Defendant name too low: y={y}")
        self.assertLessEqual(y, DEFENDANT_NAME_Y_MAX, f"Defendant name too high: y={y}")

    def test_where_city_placed_in_where_section(self) -> None:
        """WHERE city must land near the CITY/TOWN/MUNICIPALITY label (y between 425 and 455)."""

        payload = self.build_case_payload(is_complete=True)
        payload["claim"]["location"]["city"] = "Vancouver"
        pdf_path = self._render_to_tmpdir(payload)
        positions = self.extract_page_text_positions(pdf_path, 3)
        # Find the user-data "Vancouver" that is in the WHERE column (x < 350, below WHERE? label).
        matching = [(y, x, t) for y, x, t in positions
                    if "Vancouver" in t and x < 350 and y < 460]
        self.assertTrue(matching, "WHERE city text not found in WHERE section x-range")
        y = matching[0][0]
        self.assertGreaterEqual(y, WHERE_CITY_Y_MIN, f"WHERE city too low: y={y}")
        self.assertLessEqual(y, WHERE_CITY_Y_MAX, f"WHERE city too high: y={y}")

    def test_when_date_placed_in_when_section(self) -> None:
        """WHEN date must land in the WHEN column (y between 405 and 445, x inside leftWhen box)."""

        pdf_path = self._render_to_tmpdir(self.build_case_payload(is_complete=True))
        positions = self.extract_page_text_positions(pdf_path, 3)
        # x > 300 covers both the leftWhen box (322–403) and rules out the facts column (x≈140).
        when_entries = [(y, x, t) for y, x, t in positions
                        if ("2026" in t or "March" in t) and x > 300]
        self.assertTrue(when_entries, "WHEN date not found in WHEN column (x > 300)")
        y, x_pos, _ = when_entries[0]
        self.assertGreaterEqual(y, WHEN_DATE_Y_MIN, f"WHEN date too low: y={y}")
        self.assertLessEqual(y, WHEN_DATE_Y_MAX, f"WHEN date too high: y={y}")
        self.assertLessEqual(
            x_pos, WHEN_DATE_X_MAX,
            f"WHEN date x={x_pos} is outside leftWhen annotation box (max x={WHEN_DATE_X_MAX})",
        )

    def test_remedy_row_a_placed_in_how_much_section(self) -> None:
        """First remedy description must land near the 'a' row in HOW MUCH (y 360–395)."""

        pdf_path = self._render_to_tmpdir(self.build_case_payload(is_complete=True))
        positions = self.extract_page_text_positions(pdf_path, 3)
        matching = [(y, x, t) for y, x, t in positions
                    if "Refund" in t and x > 100]
        self.assertTrue(matching, "First remedy description not found on notice page")
        y = matching[0][0]
        self.assertGreaterEqual(y, REMEDY_ROW_A_Y_MIN, f"Remedy row a too low: y={y}")
        self.assertLessEqual(y, REMEDY_ROW_A_Y_MAX, f"Remedy row a too high: y={y}")

    def test_total_amount_placed_at_total_row(self) -> None:
        """Total amount must land at the TOTAL row (y between 215 and 235)."""

        pdf_path = self._render_to_tmpdir(self.build_case_payload(is_complete=True))
        positions = self.extract_page_text_positions(pdf_path, 3)
        # Find the total amount (3500.00) at the TOTAL row (not the remedy row).
        total_entries = [(y, x, t) for y, x, t in positions
                         if "3500" in t and x > 400 and y < REMEDY_ROW_A_Y_MIN]
        self.assertTrue(total_entries, "Total amount not found below HOW MUCH rows")
        y = total_entries[0][0]
        self.assertGreaterEqual(y, TOTAL_Y_MIN, f"Total amount too low: y={y}")
        self.assertLessEqual(y, TOTAL_Y_MAX, f"Total amount too high: y={y}")

    def test_when_date_formatted_human_readable(self) -> None:
        """WHEN date must be formatted as a human-readable string, not raw ISO-8601."""

        pdf_path = self._render_to_tmpdir(self.build_case_payload(is_complete=True))
        page_text = self.extract_pdf_page_text(pdf_path, 3)
        self.assertNotIn("2026-03-15", page_text, "ISO date must not appear verbatim on the form")

    def test_where_text_excludes_country_code(self) -> None:
        """WHERE section must not show the country code (CA) — province is pre-printed."""

        pdf_path = self._render_to_tmpdir(self.build_case_payload(is_complete=True))
        page_text = self.extract_pdf_page_text(pdf_path, 3)
        # The country abbreviation must not appear in the rendered WHERE value.
        self.assertNotIn(", CA", page_text, "Country code must not appear in WHERE section")


    def test_facts_text_within_what_happened_section(self) -> None:
        """All rendered facts lines must land within the WHAT HAPPENED section (y 445–510).

        Uses a multi-line facts payload that triggers text wrapping to expose
        any line-spacing overflow into the WHERE/WHEN or HOW MUCH sections.
        """

        payload = self.build_case_payload(is_complete=True)
        payload["claim"]["facts"] = (
            "The defendant agreed to complete kitchen renovation work by March 15, 2026. "
            "The claimant paid a deposit of 1500 on January 10, 2026. "
            "The defendant abandoned the project on March 1, 2026 without completing "
            "the agreed work or returning the deposit."
        )
        pdf_path = self._render_to_tmpdir(payload)
        positions = self.extract_page_text_positions(pdf_path, 3)
        # Match any facts fragment at the data x-start (≥ 130) below the WHAT HAPPENED heading.
        facts_entries = [
            (y, x, t) for y, x, t in positions
            if x >= 130 and FACTS_Y_MIN <= y <= FACTS_Y_MAX
            and any(kw in t for kw in ("defendant agreed", "deposit", "abandoned"))
        ]
        self.assertTrue(facts_entries, "No facts lines found within WHAT HAPPENED y-range (445–510)")
        # Also assert that NO facts text appears below the WHAT HAPPENED section.
        overflow = [
            (y, t) for y, x, t in positions
            if x >= 130 and y < FACTS_Y_MIN
            and any(kw in t for kw in ("defendant agreed", "abandoned", "returning the deposit"))
        ]
        self.assertFalse(
            overflow,
            f"Facts lines overflowed below WHAT HAPPENED section: {overflow}",
        )

    def test_defendant_city_does_not_include_province(self) -> None:
        """The city field in the TO section must show city only, not 'City, Province'."""

        pdf_path = self._render_to_tmpdir(self.build_case_payload(is_complete=True))
        positions = self.extract_page_text_positions(pdf_path, 3)
        city_entries = [(y, x, t) for y, x, t in positions if "Burnaby" in t]
        self.assertTrue(city_entries, "Defendant city 'Burnaby' not found on notice page")
        for _, _, text in city_entries:
            self.assertNotIn(", BC", text, f"City field must not include province abbreviation: got '{text}'")

    def test_defendant_postal_in_postal_column(self) -> None:
        """Postal code must land in the postal column (x > 250), not the city/address column."""

        pdf_path = self._render_to_tmpdir(self.build_case_payload(is_complete=True))
        positions = self.extract_page_text_positions(pdf_path, 3)
        postal_entries = [(y, x, t) for y, x, t in positions if "V5C" in t]
        self.assertTrue(postal_entries, "Defendant postal code 'V5C 2B2' not found on notice page")
        for _, x, _ in postal_entries:
            self.assertGreater(
                x, TO_POSTAL_X_MIN,
                f"Postal code x={x} must be > {TO_POSTAL_X_MIN} (postal column, not city column)",
            )

    def test_defendant_phone_rendered_in_to_section(self) -> None:
        """Defendant phone number must appear on the notice page when provided at the defendant level."""

        payload = self.build_case_payload(is_complete=True)
        payload["defendants"][0]["phone"] = "604-555-1234"
        pdf_path = self._render_to_tmpdir(payload)
        page_text = self.extract_pdf_page_text(pdf_path, 3)
        self.assertIn("604-555-1234", page_text, "Defendant phone not rendered on notice page")


if __name__ == "__main__":
    unittest.main()