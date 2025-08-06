import json
from typing import Dict

from cpc_tree import load_cpc_tree, CPCTreeNode, build_cpc_tree


def test_build_cpc_tree():
    """Test building the CPC tree from XML files."""
    cpc_tree = build_cpc_tree("CPCSchemeXML202508")

    assert "A" in cpc_tree
    assert cpc_tree["A"]["title"] == "HUMAN NECESSITIES"
    assert "children" in cpc_tree["A"]
    assert "A01" in cpc_tree["A"]["children"]

    a01_node = cpc_tree["A"]["children"]["A01"]
    assert (
        a01_node["title"]
        == "AGRICULTURE"
    )
    assert "children" in a01_node
    assert "A01B" in a01_node["children"]

    a01b_node = a01_node["children"]["A01B"]
    assert (
        a01b_node["title"]
        == "SOIL WORKING IN AGRICULTURE OR FORESTRY; PARTS, DETAILS, OR ACCESSORIES OF AGRICULTURAL MACHINES OR IMPLEMENTS, IN GENERAL"
    )
    assert "children" in a01b_node
    assert "A01B 1/00" in a01b_node["children"]

    a01b_1_00_node = a01b_node["children"]["A01B 1/00"]
    assert a01b_1_00_node["title"] == "Hand tools (edge trimmers for lawns A01G3/06)"
    assert "children" not in a01b_1_00_node


def test_load_cpc_tree():
    """Test loading the CPC tree from a dictionary into CPCTreeNode objects."""
    cpc_data = {
        "A": {
            "title": "HUMAN NECESSITIES",
            "children": {
                "A01": {
                    "title": "AGRICULTURE; FORESTRY; ANIMAL HUSBANDRY; HUNTING; TRAPPING; FISHING",
                    "children": {
                        "A01B": {
                            "title": "SOIL WORKING IN AGRICULTURE OR FORESTRY; PARTS, DETAILS, OR ACCESSORIES OF AGRICULTURAL MACHINES OR IMPLEMENTS, IN GENERAL"
                        }
                    },
                }
            },
        }
    }

    cpc_tree: Dict[str, CPCTreeNode] = {}
    for key, value in cpc_data.items():
        node = load_cpc_tree(value)
        if node is not None:
            cpc_tree[key] = node

    assert "A" in cpc_tree
    root_node = cpc_tree["A"]
    assert isinstance(root_node, CPCTreeNode)
    assert root_node.title == "HUMAN NECESSITIES"
    assert "A01" in root_node.children

    a01_node = root_node.children["A01"]
    assert isinstance(a01_node, CPCTreeNode)
    assert (
        a01_node.title
        == "AGRICULTURE; FORESTRY; ANIMAL HUSBANDRY; HUNTING; TRAPPING; FISHING"
    )
    assert "A01B" in a01_node.children

    a01b_node = a01_node.children["A01B"]
    assert isinstance(a01b_node, CPCTreeNode)
    assert (
        a01b_node.title
        == "SOIL WORKING IN AGRICULTURE OR FORESTRY; PARTS, DETAILS, OR ACCESSORIES OF AGRICULTURAL MACHINES OR IMPLEMENTS, IN GENERAL"
    )
    assert not a01b_node.children


def test_end_to_end(tmp_path):
    """Test the end-to-end process of building and then loading the CPC tree."""

    # Build the tree from XML
    built_tree = build_cpc_tree("CPCSchemeXML202508")
    
    # Save to a temporary JSON file (as an intermediate step)
    json_path = tmp_path / "cpc_tree.json"
    with open(json_path, "w") as f:
        json.dump(built_tree, f)

    # Load the data from JSON
    with open(json_path, "r") as f:
        cpc_data = json.load(f)

    # Load into CPCTreeNode objects
    cpc_tree: Dict[str, CPCTreeNode] = {}
    for key, value in cpc_data.items():
        node = load_cpc_tree(value)
        if node is not None:
            cpc_tree[key] = node

    # Assertions similar to the other tests
    assert "A" in cpc_tree
    root_node = cpc_tree["A"]
    assert isinstance(root_node, CPCTreeNode)
    assert root_node.title == "HUMAN NECESSITIES"

    assert "A01" in root_node.children
    a01_node = root_node.children["A01"]
    assert (
        a01_node.title
        == "AGRICULTURE"
    )

    assert "A01B" in a01_node.children
    a01b_node = a01_node.children["A01B"]
    assert (
        a01b_node.title
        == "SOIL WORKING IN AGRICULTURE OR FORESTRY; PARTS, DETAILS, OR ACCESSORIES OF AGRICULTURAL MACHINES OR IMPLEMENTS, IN GENERAL"
    )

    assert "A01B 1/00" in a01b_node.children
    a01b_1_00_node = a01b_node.children["A01B 1/00"]
    assert a01b_1_00_node.title == "Hand tools (edge trimmers for lawns A01G3/06)"
    assert not a01b_1_00_node.children
