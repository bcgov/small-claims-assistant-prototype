# Purpose: Validate canonical Notice of Claim JSON and emit deterministic PDF-generation artifacts.

"""Deterministic Notice of Claim renderer scaffold."""

from __future__ import annotations

import argparse
import io
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

from datetime import datetime

from pypdf import PdfReader, PdfWriter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


HERE = Path(__file__).resolve().parent
PLUGIN_ROOT = HERE.parent
TEMPLATE_PATH = (
    PLUGIN_ROOT
    / "assets"
    / "templates"
    / "forms"
    / "small-claims"
    / "scl001-notice-of-claim-template.pdf"
)
NOTICE_PAGE_INDEXES = {2}
PAGE_WIDTH = 612
PAGE_HEIGHT = 792

# ── Form field anchor coordinates derived from template text-position analysis ──
# All y values are PDF coordinates (origin bottom-left, y increases upward).
# Calibrated against the official SCL 001 10/2022 template (612 × 792 pt).

# FROM section — claimant name only (address goes on Form 38).
# Writing line at y=685.021; text baseline = line_y + 0.8 → 686.
_FROM_NAME_Y = 686.0
_FROM_NAME_X = 140.0

# Registry boxes (upper-right).
_REGISTRY_LOCATION_Y = 726.0
_REGISTRY_LOCATION_X = 480.0

# TO section — defendant name, address lines, city/prov/postal, and phone.
# Writing lines extracted from template graphics stream (text_y = line_y + 0.8):
#   NAME line y=609.724 → text y=610, ADDRESS line y=588.141 → text y=589, CITY line y=561.195 → text y=562.
_TO_NAME_Y = 610.0
_TO_ADDRESS_Y = 589.0
_TO_CITY_Y = 562.0
_TO_PROV_POSTAL_Y = 547.0
_TO_PROV_X = 283.0       # province starts just inside the PROV. label (x=275.7)
_TO_POSTAL_X = 355.0     # postal code starts in the POSTAL CODE column
_TO_PHONE_X = 490.0
_TO_DATA_X = 140.0

# WHAT HAPPENED — facts text area (y=450–507; 5 lines max to avoid overflow).
_FACTS_START_Y = 495.0
_FACTS_MAX_LINES = 5
_FACTS_X = 140.0
_FACTS_MAX_WIDTH = 430.0

# WHERE / WHEN — city only (province pre-printed); WHEN data goes RIGHT of leftWhen sidebar (x=405.8–578.6).
# WHERE/WHEN share the same writing line: y=441.342 → text y=442.
# leftWhen sidebar rect=[322.0, 400.6, 402.9, 439.7] is the WHEN? label — data starts at x=405.8.
_WHERE_CITY_Y = 442.0
_WHERE_CITY_X = 140.0
_WHEN_DATE_Y = 442.0   # same writing line as WHERE city
_WHEN_DATE_X = 408.0   # just inside WHEN data field (field x=405.8..578.6)

# HOW MUCH — remedy rows a–e and sub-total.
# Each tuple is (description_y, amount_y) calibrated to template writing lines.
# Desc lines (form): 384.973, 351.921, 318.869, 288.028, 254.182 → text = line + 1.
# Amt lines (form):  372.974, 339.922, 306.870, 274.198, 241.390 → text = line + 3 (confirmed by existing tests).
_REMEDY_ROW_ANCHORS = [
    (386.0, 376.0),   # row a  (desc line y=384.973, amt line y=372.974)
    (353.0, 343.0),   # row b  (desc line y=351.921, amt line y=339.922)
    (320.0, 310.0),   # row c  (desc line y=318.869, amt line y=306.870)
    (289.0, 277.0),   # row d  (desc line y=288.028, amt line y=274.198)
    (255.0, 245.0),   # row e  (desc line y=254.182, amt line y=241.390)
]
_REMEDY_DESC_X = 132.0
_REMEDY_AMOUNT_RIGHT_X = 548.0
_TOTAL_Y = 225.0   # TOTAL row (label y=226.8, $ y=225.5)


# Keep file loading deterministic and isolated from host-specific state.
def load_case_payload(input_path: Path) -> dict[str, Any]:
    """Read the canonical case JSON from disk."""

    return json.loads(input_path.read_text(encoding="utf-8"))


# Enforce the intake-to-JSON versus JSON-to-PDF boundary at the renderer entrypoint.
def validate_ready_for_pdf(case_data: dict[str, Any]) -> None:
    """Reject canonical case drafts that are not yet ready for deterministic generation."""

    validation = case_data.get("validation", {})
    generation = case_data.get("generation", {}).get("pdf", {})
    case_status = case_data.get("caseMetadata", {}).get("status")

    if not validation.get("isComplete"):
        raise ValueError("Case is not ready for PDF generation: validation.isComplete must be true.")

    if not generation.get("ready"):
        raise ValueError("Case is not ready for PDF generation: generation.pdf.ready must be true.")

    if case_status not in {"ready-for-pdf", "generated"}:
        raise ValueError("Case is not ready for PDF generation: caseMetadata.status must be ready-for-pdf or generated.")


# Keep PDF text placement predictable by normalizing structured case data into printable strings.
def flatten_address(contact: dict[str, Any]) -> list[str]:
    """Return a mailing address as printable lines."""

    address_lines = [line for line in contact.get("addressLines", []) if line]
    city_parts = [contact.get("city"), contact.get("province"), contact.get("postalCode")]
    city_line = ", ".join(part for part in city_parts[:2] if part)
    if city_parts[2]:
        city_line = f"{city_line} {city_parts[2]}".strip()
    if city_line:
        address_lines.append(city_line)
    return address_lines


# Convert the canonical claim date object into one concise human-readable string.
def format_incident_date(incident_date: dict[str, Any]) -> str:
    """Return the claim date or date range as a human-readable string (e.g. March 15, 2026)."""

    if not incident_date:
        return ""

    date_type = incident_date.get("type")
    start = incident_date.get("start", "")
    end = incident_date.get("end", "")

    def _parse(iso: str) -> str:
        try:
            return datetime.strptime(iso, "%Y-%m-%d").strftime("%B %d, %Y")
        except ValueError:
            return iso

    if date_type == "range" and start and end:
        return f"{_parse(start)} to {_parse(end)}"

    return _parse(start)


# Keep money presentation stable across tests and downstream review.
def format_money(value: float) -> str:
    """Return a currency value in fixed two-decimal form."""

    return f"{value:.2f}"


# Simple width-based wrapping is sufficient for the first deterministic overlay slice.
def wrap_text(text: str, *, font_name: str, font_size: int, max_width: float) -> list[str]:
    """Wrap text into printable lines for a fixed-width form region."""

    if not text:
        return []

    wrapped_lines: list[str] = []
    paragraphs = [paragraph.strip() for paragraph in text.splitlines() if paragraph.strip()]
    for paragraph in paragraphs:
        current_line = ""
        for word in paragraph.split():
            candidate = word if not current_line else f"{current_line} {word}"
            if stringWidth(candidate, font_name, font_size) <= max_width:
                current_line = candidate
                continue

            if current_line:
                wrapped_lines.append(current_line)
            current_line = word

        if current_line:
            wrapped_lines.append(current_line)

    return wrapped_lines


# All drawing helpers write text overlays only; the official template remains the page background.
def draw_lines(pdf: canvas.Canvas, *, lines: list[str], x: float, y: float, leading: float, font_size: int) -> None:
    """Draw multiple lines of text from a top-left anchor."""

    text_object = pdf.beginText(x, y)
    text_object.setFont("Helvetica", font_size)
    text_object.setLeading(leading)
    for line in lines:
        text_object.textLine(line)
    pdf.drawText(text_object)


# Render the main notice page overlay for one copy of the form package.
def draw_notice_page(pdf: canvas.Canvas, case_data: dict[str, Any]) -> None:
    """Overlay claimant, defendant, facts, where/when, and remedies onto the notice form page.

    Coordinate system: PDF origin is bottom-left; y increases upward.
    All anchor constants are calibrated against the SCL 001 10/2022 template (612 × 792 pt).
    """

    claimant = (case_data.get("claimants") or [{}])[0]
    defendant = (case_data.get("defendants") or [{}])[0]
    claim = case_data.get("claim", {})
    remedies = case_data.get("remedies", [])
    jurisdiction = case_data.get("jurisdiction", {})

    pdf.setFont("Helvetica", 9)

    # ── Registry location (upper-right box, below REGISTRY LOCATION label) ──
    registry_location = str(jurisdiction.get("registryLocation", ""))
    if registry_location:
        pdf.drawString(_REGISTRY_LOCATION_X, _REGISTRY_LOCATION_Y, registry_location)

    # ── FROM section — claimant name only; address is on Form 38 ──
    claimant_name = claimant.get("name", {}).get("full", "")
    if claimant_name:
        pdf.drawString(_FROM_NAME_X, _FROM_NAME_Y, claimant_name)

    # ── TO section — defendant name, address, city/prov/postal, phone ──
    defendant_name = defendant.get("name", {}).get("full", "")
    if defendant_name:
        pdf.drawString(_TO_DATA_X, _TO_NAME_Y, defendant_name)

    def_contact = defendant.get("contact", {})
    def_street_lines = [ln for ln in def_contact.get("addressLines", []) if ln]
    def_city = def_contact.get("city", "")
    def_prov = def_contact.get("province", "")
    def_postal = def_contact.get("postalCode", "")
    # Phone may be at the defendant top-level (canonical schema) or inside contact.
    def_phone = defendant.get("phone", "") or def_contact.get("phone", "")

    if def_street_lines:
        pdf.drawString(_TO_DATA_X, _TO_ADDRESS_Y, def_street_lines[0])
    if def_city:
        pdf.drawString(_TO_DATA_X, _TO_CITY_Y, def_city)          # city only — no province
    if def_prov:
        pdf.drawString(_TO_PROV_X, _TO_CITY_Y, def_prov)          # province on same writing line as city
    if def_postal:
        pdf.drawString(_TO_POSTAL_X, _TO_CITY_Y, def_postal)      # postal on same writing line as city
    if def_phone:
        pdf.drawString(_TO_PHONE_X, _TO_CITY_Y, def_phone)

    # ── WHAT HAPPENED — facts narrative, clipped to available section height ──
    facts_text = claim.get("facts", "")
    fact_lines = wrap_text(facts_text, font_name="Helvetica", font_size=9, max_width=_FACTS_MAX_WIDTH)
    fact_lines = fact_lines[:_FACTS_MAX_LINES]
    for i, line in enumerate(fact_lines):
        pdf.drawString(_FACTS_X, _FACTS_START_Y - i * 11, line)

    # ── WHERE — city only; province (British Columbia) is pre-printed on the form ──
    where_city = claim.get("location", {}).get("city", "")
    if where_city:
        pdf.drawString(_WHERE_CITY_X, _WHERE_CITY_Y, where_city)

    # ── WHEN — incident date formatted as human-readable string ──
    when_text = format_incident_date(claim.get("incidentDate", {}))
    if when_text:
        pdf.drawString(_WHEN_DATE_X, _WHEN_DATE_Y, when_text)

    # ── HOW MUCH — remedy rows and sub-total ──
    total_amount = 0.0
    for row_index, remedy in enumerate(remedies[:5]):
        if row_index >= len(_REMEDY_ROW_ANCHORS):
            break
        desc_y, amt_y = _REMEDY_ROW_ANCHORS[row_index]
        description = remedy.get("description", "")
        amount_value = float(remedy.get("amount", {}).get("value", 0.0) or 0.0)
        wrapped_desc = wrap_text(description, font_name="Helvetica", font_size=9, max_width=360)
        pdf.drawString(_REMEDY_DESC_X, desc_y, (wrapped_desc[:1] or [""])[0])
        pdf.drawRightString(_REMEDY_AMOUNT_RIGHT_X, amt_y, format_money(amount_value))
        total_amount += amount_value

    pdf.drawRightString(_REMEDY_AMOUNT_RIGHT_X, _TOTAL_Y, format_money(total_amount))


# Build an overlay PDF in memory so the official template can remain the static background.
def build_overlay(case_data: dict[str, Any], page_count: int) -> io.BytesIO:
    """Create a page-aligned overlay PDF for the notice package."""

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

    for page_index in range(page_count):
        if page_index in NOTICE_PAGE_INDEXES:
            draw_notice_page(pdf, case_data)
        pdf.showPage()

    pdf.save()
    buffer.seek(0)
    return buffer


# Emit a rendered package by merging the case-data overlay onto the official template.
def render_pdf_package(case_data: dict[str, Any], output_dir: Path) -> Path:
    """Render the notice package PDF into the target directory."""

    output_dir.mkdir(parents=True, exist_ok=True)
    package_path = output_dir / "notice-of-claim-package.pdf"

    template_reader = PdfReader(str(TEMPLATE_PATH))
    overlay_reader = PdfReader(build_overlay(case_data, len(template_reader.pages)))
    writer = PdfWriter()

    for page_index, template_page in enumerate(template_reader.pages):
        page = template_page
        overlay_page = overlay_reader.pages[page_index]
        page.merge_page(overlay_page)
        writer.add_page(page)

    writer.write(package_path)
    return package_path


# Return machine-readable generation metadata for downstream orchestration and review.
def build_manifest(case_data: dict[str, Any], package_path: Path) -> dict[str, Any]:
    """Build the deterministic artifact manifest for the renderer output."""

    template_version = (
        case_data.get("generation", {})
        .get("pdf", {})
        .get("templateVersion", "bc-scc-form1-v1")
    )

    return {
        "status": "generated",
        "formType": case_data.get("formType"),
        "templateVersion": template_version,
        "artifacts": [
            {
                "kind": "package-pdf",
                "path": str(package_path),
            }
        ],
        "notes": [
            "Rendered notice pages are overlaid onto the archived Form 1 package template.",
            "Long-form overflow handling and companion-page refinement remain separate follow-on work.",
        ],
    }


# Persist the manifest beside the generated artifact for later workflow handoff.
def write_manifest(output_dir: Path, manifest: dict[str, Any]) -> Path:
    """Write the render manifest to disk."""

    manifest_path = output_dir / "render-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return manifest_path


# Keep the CLI surface narrow and deterministic so skills can call one stable renderer entrypoint.
def main() -> int:
    """Run readiness validation and emit the first deterministic PDF-generation artifacts."""

    parser = argparse.ArgumentParser(
        description="Render a deterministic BC Notice of Claim PDF artifact scaffold from canonical JSON."
    )
    parser.add_argument("--input", required=True, help="Path to the canonical case JSON file.")
    parser.add_argument("--output-dir", required=True, help="Directory for generated PDF artifacts.")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)

    try:
        case_data = load_case_payload(input_path)
        validate_ready_for_pdf(case_data)
        package_path = render_pdf_package(case_data, output_dir)
        manifest = build_manifest(case_data, package_path)
        write_manifest(output_dir, manifest)
    except Exception as exc:  # pragma: no cover - exercised through subprocess tests.
        print(str(exc), file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())