import argparse
import json
from typing import Any, Dict

from . import build_cpc_tree


def main() -> None:
    """Build the CPC tree from XML files and write it to cpc_tree.json."""
    parser = argparse.ArgumentParser(
        description="Build the CPC tree from XML files."
    )
    parser.add_argument(
        "xml_directory",
        type=str,
        help="Path to the directory containing CPC XML files (should include cpc-scheme.xml)",
    )
    args = parser.parse_args()
    xml_dir: str = args.xml_directory
    cpc_tree: Dict[str, Any] = build_cpc_tree(xml_dir)
    with open("cpc_tree.json", "w", encoding="utf-8") as f:
        json.dump(cpc_tree, f, indent=4)


if __name__ == "__main__":
    main()
