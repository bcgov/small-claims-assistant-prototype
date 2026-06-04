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


# Convert the canonical claim date object into one concise string for the court form.
def format_incident_date(incident_date: dict[str, Any]) -> str:
    """Return the claim date or date range as printed text."""

    if not incident_date:
        return ""

    date_type = incident_date.get("type")
    start = incident_date.get("start", "")
    end = incident_date.get("end", "")

    if date_type == "range" and start and end:
        return f"{start} to {end}"

    return start


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
    """Overlay the claimant, defendant, facts, and remedies onto one notice form page."""

    claimant = (case_data.get("claimants") or [{}])[0]
    defendant = (case_data.get("defendants") or [{}])[0]
    claim = case_data.get("claim", {})
    remedies = case_data.get("remedies", [])
    jurisdiction = case_data.get("jurisdiction", {})

    claimant_lines = [claimant.get("name", {}).get("full", "")]
    claimant_lines.extend(flatten_address(claimant.get("contact", {})))

    defendant_lines = [defendant.get("name", {}).get("full", "")]
    defendant_lines.extend(flatten_address(defendant.get("contact", {})))

    detail_text = claim.get("facts", "")
    detail_lines = wrap_text(detail_text, font_name="Helvetica", font_size=9, max_width=430)
    detail_lines = detail_lines[:18]

    where_text = ", ".join(
        part for part in [
            claim.get("location", {}).get("city"),
            claim.get("location", {}).get("province"),
            claim.get("location", {}).get("country"),
        ] if part
    )
    when_text = format_incident_date(claim.get("incidentDate", {}))

    remedy_lines = remedies[:5]
    total_amount = sum(
        float(remedy.get("amount", {}).get("value", 0.0))
        for remedy in remedies
        if remedy.get("amount", {}).get("value") is not None
    )

    pdf.setFont("Helvetica", 9)
    pdf.drawString(480, 734, str(jurisdiction.get("registryLocation", "")))

    draw_lines(pdf, lines=claimant_lines, x=140, y=646, leading=11, font_size=9)
    draw_lines(pdf, lines=defendant_lines, x=140, y=612, leading=11, font_size=9)
    draw_lines(pdf, lines=detail_lines, x=156, y=492, leading=11, font_size=9)
    pdf.drawString(108, 326, where_text)
    pdf.drawString(442, 326, when_text)

    row_y = 264
    for remedy in remedy_lines:
        description = remedy.get("description", "")
        amount_value = float(remedy.get("amount", {}).get("value", 0.0))
        wrapped_description = wrap_text(description, font_name="Helvetica", font_size=9, max_width=360)
        wrapped_description = wrapped_description[:1] or [""]
        pdf.drawString(132, row_y, wrapped_description[0])
        pdf.drawRightString(548, row_y, format_money(amount_value))
        row_y -= 21

    pdf.drawRightString(548, 84, format_money(total_amount))


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