import argparse
import json
import logging
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import xml.etree.ElementTree as ET


@dataclass
class CPCTreeNode:
    code: str
    title: Optional[str] = None
    children: Dict[str, "CPCTreeNode"] = field(default_factory=dict)


def load_cpc_tree(data: Dict[str, Any]) -> Dict[str, "CPCTreeNode"]:
    """Recursively loads a CPC tree from a nested dictionary."""

    def _load_node(code: str, node_data: Dict[str, Any]) -> "CPCTreeNode":
        children_data = node_data.get("children", {})
        children = {
            child_code: _load_node(child_code, child_data)
            for child_code, child_data in children_data.items()
        }
        return CPCTreeNode(code=code, title=node_data.get("title"), children=children)

    return {code: _load_node(code, node_data) for code, node_data in data.items()}


def get_title(element: ET.Element) -> str:
    """Extracts and joins all text from <class-title>/<title-part>/<text> elements."""
    title_parts: List[ET.Element] = element.findall("class-title/title-part/text")
    return (
        " ".join([part.text for part in title_parts if part.text])
        if title_parts
        else ""
    )


def parse_item(item_element: ET.Element, directory: str) -> Dict[str, Any]:
    """Parse a classification-item element and its children recursively."""
    node: Dict[str, Any] = {}
    title: str = get_title(item_element)
    if title:
        node["title"] = title

    children: Dict[str, Any] = {}

    link_file: Optional[str] = item_element.get("link-file")
    if link_file:
        children = _parse_linked_children(link_file, directory)
    else:
        children = _parse_direct_children(item_element, directory)

    if children:
        node["children"] = children

    return node


def _parse_linked_children(link_file: str, directory: str) -> Dict[str, Any]:
    """Parse children from a linked XML file."""
    children: Dict[str, Any] = {}
    file_path: str = os.path.join(directory, link_file)
    if os.path.exists(file_path):
        try:
            tree: ET.ElementTree = ET.parse(file_path)  # type: ignore
            root: Optional[ET.Element] = tree.getroot()
            root_item: Optional[ET.Element] = (
                root.find("./classification-item") if root is not None else None
            )
            if root_item is not None:
                for sub_item in root_item.findall("./classification-item"):
                    symbol_element: Optional[ET.Element] = sub_item.find(
                        "classification-symbol"
                    )
                    if symbol_element is not None and symbol_element.text:
                        symbol: str = symbol_element.text
                        children[symbol] = parse_item(sub_item, directory)
        except ET.ParseError:
            logging.info(f"Skipping malformed file: {file_path}")
    return children


def _parse_direct_children(item_element: ET.Element, directory: str) -> Dict[str, Any]:
    """Parse children directly from the current XML element."""
    children: Dict[str, Any] = {}
    for sub_item in item_element.findall("./classification-item"):
        symbol_element: Optional[ET.Element] = sub_item.find("classification-symbol")
        if symbol_element is not None and symbol_element.text:
            symbol: str = symbol_element.text
            children[symbol] = parse_item(sub_item, directory)
    return children


def build_cpc_tree(directory: str) -> Dict[str, Any]:
    """Build the CPC tree from the XML files in the given directory."""
    main_xml_path: str = os.path.join(directory, "cpc-scheme.xml")
    main_tree: ET.ElementTree = ET.parse(main_xml_path)  # type: ignore
    main_root: Optional[ET.Element] = main_tree.getroot()
    cpc_tree: Dict[str, Any] = {}

    for top_level_item in main_root.findall("./classification-item"):  # type: ignore
        symbol_element: Optional[ET.Element] = top_level_item.find(
            "classification-symbol"
        )
        if symbol_element is not None and symbol_element.text:
            symbol: str = symbol_element.text
            cpc_tree[symbol] = parse_item(top_level_item, directory)

    return cpc_tree


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    parser = argparse.ArgumentParser(description="Build the CPC tree from XML files.")
    parser.add_argument(
        "xml_directory",
        type=str,
        help="Path to the directory containing CPC XML files (should include cpc-scheme.xml)",
    )
    args = parser.parse_args()
    xml_dir: str = args.xml_directory
    cpc_tree: Dict[str, Any] = build_cpc_tree(xml_dir)
    with open("cpc_tree.json", "w+") as f:
        json.dump(cpc_tree, f, indent=4)
