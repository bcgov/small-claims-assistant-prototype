# Purpose: Validate canonical Notice of Claim JSON and emit deterministic PDF-generation artifacts.

"""Deterministic Notice of Claim renderer scaffold."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any


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


# Emit a deterministic initial package artifact while the full field-binding renderer is still being built.
def render_pdf_package(output_dir: Path) -> Path:
    """Copy the archived Form 1 template into the output directory as the first package artifact."""

    output_dir.mkdir(parents=True, exist_ok=True)
    package_path = output_dir / "notice-of-claim-package.pdf"
    shutil.copyfile(TEMPLATE_PATH, package_path)
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
            "Current renderer slice emits the archived Form 1 template package scaffold.",
            "Field binding, overflow handling, and companion-page assembly remain separate follow-on work.",
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
        package_path = render_pdf_package(output_dir)
        manifest = build_manifest(case_data, package_path)
        write_manifest(output_dir, manifest)
    except Exception as exc:  # pragma: no cover - exercised through subprocess tests.
        print(str(exc), file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())