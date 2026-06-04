from __future__ import annotations

import argparse
import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PLUGIN_ROOT = HERE.parent
DEFINITION_PATH = (
    PLUGIN_ROOT
    / "assets"
    / "case-models"
    / "notice-of-claim"
    / "notice-of-claim-intake-definition.json"
)


def load_definition() -> dict[str, Any]:
    return json.loads(DEFINITION_PATH.read_text(encoding="utf-8"))


def deep_merge(base: Any, patch: Any) -> Any:
    if isinstance(base, dict) and isinstance(patch, dict):
        merged = deepcopy(base)
        for key, value in patch.items():
            if key in merged:
                merged[key] = deep_merge(merged[key], value)
            else:
                merged[key] = deepcopy(value)
        return merged

    if isinstance(base, list) and isinstance(patch, list):
        return deepcopy(patch)

    return deepcopy(patch)


def apply_defaults(case_data: dict[str, Any]) -> dict[str, Any]:
    definition = load_definition()
    template = deepcopy(definition["canonicalDraftTemplate"])
    merged = deep_merge(template, case_data)

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    case_metadata = merged.setdefault("caseMetadata", {})
    case_metadata.setdefault("status", "draft")
    case_metadata.setdefault("intakeChannel", "plugin")
    case_metadata.setdefault("language", "en")
    case_metadata["updatedAt"] = now
    if not case_metadata.get("createdAt"):
        case_metadata["createdAt"] = now

    merged.setdefault("validation", {}).setdefault("missingFields", [])
    merged.setdefault("validation", {}).setdefault("warnings", [])
    merged.setdefault("validation", {}).setdefault("isComplete", False)
    return merged


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Write a deterministic BC Notice of Claim canonical JSON file from a partial patch payload."
    )
    parser.add_argument("--input", required=True, help="Path to a JSON patch payload.")
    parser.add_argument("--output", required=True, help="Path to write the canonical JSON output.")
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Write indented JSON for review instead of compact JSON.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    patch_payload = json.loads(input_path.read_text(encoding="utf-8"))
    merged = apply_defaults(patch_payload)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(merged, indent=2 if args.pretty else None, ensure_ascii=True)
    if args.pretty:
        text += "\n"
    output_path.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())