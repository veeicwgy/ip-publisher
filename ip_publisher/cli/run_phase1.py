from __future__ import annotations

import argparse
import json
from pathlib import Path

from ..workflows.phase1_generate_and_audit import run_phase1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 1 KB-driven generation and audit workflow")
    parser.add_argument("--request", required=True, help="Path to article_request JSON")
    parser.add_argument("--kb-dir", default="data/kb_raw", help="Knowledge-base input directory")
    parser.add_argument("--index-db", default="data/kb_index/phase1.db", help="SQLite FTS index path")
    parser.add_argument("--output-root", default="outputs", help="Artifact output directory")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_phase1(
        request_path=Path(args.request),
        kb_dir=Path(args.kb_dir),
        index_db=Path(args.index_db),
        output_root=Path(args.output_root),
    )
    print(json.dumps(result["artifacts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
