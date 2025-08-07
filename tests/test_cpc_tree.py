import os
import xml.etree.ElementTree as ET

import pytest

from cpc_tree import (
    CPCTreeNode,
    build_cpc_tree,
    get_title,
    load_cpc_tree,
    parse_item,
)

DATA_DIR = "CPCSchemeXML202508"


def test_get_title():
    """Test the get_title function with a sample XML element."""
    xml_string = """
    <classification-item>
        <class-title>
            <title-part><text>Part 1</text></title-part>
            <title-part><text>Part 2</text></title-part>
        </class-title>
    </classification-item>
    """
    element = ET.fromstring(xml_string)
    assert get_title(element) == "Part 1 Part 2"


def test_get_title_no_title():
    """Test get_title with an element that has no title."""
    xml_string = "<classification-item></classification-item>"
    element = ET.fromstring(xml_string)
    assert get_title(element) == ""


def test_parse_item_with_title(temp_xml_dir):
    """Test parsing an item that has a title."""
    xml_string = """
    <classification-item>
        <classification-symbol>A</classification-symbol>
        <class-title>
            <title-part><text>A Title</text></title-part>
        </class-title>
    </classification-item>
    """
    element = ET.fromstring(xml_string)
    parsed = parse_item(element, str(temp_xml_dir))
    assert parsed["title"] == "A Title"


def test_parse_item_with_direct_children(temp_xml_dir):
    """Test parsing an item with direct children."""
    xml_string = """
    <classification-item>
        <classification-symbol>A</classification-symbol>
        <classification-item>
            <classification-symbol>A01</classification-symbol>
        </classification-item>
    </classification-item>
    """
    element = ET.fromstring(xml_string)
    parsed = parse_item(element, str(temp_xml_dir))
    assert "A01" in parsed["children"]


def test_build_cpc_tree_mock(temp_xml_dir):
    """Test building the CPC tree from mock XML files."""
    cpc_tree = build_cpc_tree(str(temp_xml_dir))

    # Test top-level nodes
    assert "A" in cpc_tree
    assert "B" in cpc_tree

    # Test 'A' branch
    assert cpc_tree["A"]["title"] == "HUMAN NECESSITIES"
    assert "A01" in cpc_tree["A"]["children"]

    # Test 'B' branch with linked file
    assert "B01" in cpc_tree["B"]["children"]
    b01 = cpc_tree["B"]["children"]["B01"]
    assert b01 is not None


def test_build_cpc_tree_file_not_found(tmp_path):
    """Test building the tree when the main XML file is not found."""
    with pytest.raises(FileNotFoundError):
        build_cpc_tree(str(tmp_path))


def test_load_cpc_tree_simple():
    """Test loading a simple CPC tree from a dictionary."""
    data = {
        "A": {
            "title": "A-Title",
            "children": {
                "A01": {"title": "A01-Title"},
            },
        }
    }
    tree = load_cpc_tree(data)
    assert "A" in tree
    assert isinstance(tree["A"], CPCTreeNode)
    assert tree["A"].title == "A-Title"
    assert "A01" in tree["A"].children


@pytest.mark.skipif(not os.path.isdir(DATA_DIR), reason="CPC XML dataset not available")
def test_build_cpc_tree_integration():
    """Integration test with the full dataset."""
    cpc_tree = build_cpc_tree(DATA_DIR)
    assert "A" in cpc_tree
    assert "A01" in cpc_tree["A"]["children"]


@pytest.mark.skipif(not os.path.isdir(DATA_DIR), reason="CPC XML dataset not available")
def test_load_cpc_tree_integration():
    """Test loading the full CPC tree into CPCTreeNode objects."""
    cpc_tree_data = build_cpc_tree(DATA_DIR)
    cpc_tree = load_cpc_tree(cpc_tree_data)
    assert "A" in cpc_tree
    root_node = cpc_tree["A"]
    assert root_node.title == "HUMAN NECESSITIES"
    assert "A01" in root_node.children


def test_parse_item_with_malformed_linked_file(tmp_path):
    """Test parsing an item with a link to a malformed XML file."""
    malformed_xml_content = "<root><unclosed-tag>"
    malformed_file = tmp_path / "malformed.xml"
    malformed_file.write_text(malformed_xml_content)

    xml_string = f"""
    <classification-item link-file="{malformed_file.name}">
        <classification-symbol>A</classification-symbol>
    </classification-item>
    """
    element = ET.fromstring(xml_string)
    parsed = parse_item(element, str(tmp_path))
    assert "children" not in parsed


def test_get_title_with_empty_text():
    """Test get_title with a title part that has empty text."""
    xml_string = """
    <classification-item>
        <class-title>
            <title-part><text>Part 1</text></title-part>
            <title-part><text></text></title-part>
            <title-part><text>Part 2</text></title-part>
        </class-title>
    </classification-item>
    """
    element = ET.fromstring(xml_string)
    assert get_title(element) == "Part 1 Part 2"


def test_parse_item_with_no_symbol(temp_xml_dir):
    """Test parsing a classification-item with no classification-symbol."""
    xml_string = """
    <classification-item>
        <classification-item>
            <class-title>
                <title-part><text>A Title</text></title-part>
            </class-title>
        </classification-item>
    </classification-item>
    """
    element = ET.fromstring(xml_string)
    parsed = parse_item(element, str(temp_xml_dir))
    assert parsed is not None


def test_parse_item_with_broken_link_file(tmp_path):
    """Test parsing an item with a link to a non-existent file."""
    xml_string = """
    <classification-item link-file="nonexistent.xml">
        <classification-symbol>A</classification-symbol>
    </classification-item>
    """
    element = ET.fromstring(xml_string)
    parsed = parse_item(element, str(tmp_path))
    assert "children" not in parsed


def test_build_cpc_tree_with_no_symbol_in_main(tmp_path):
    """Test building the CPC tree when a top-level item has no symbol."""
    xml_content = """
    <cpc-scheme>
        <classification-item>
            <class-title><title-part><text>No Symbol</text></title-part></class-title>
        </classification-item>
    </cpc-scheme>
    """
    main_file = tmp_path / "cpc-scheme.xml"
    main_file.write_text(xml_content)
    tree = build_cpc_tree(str(tmp_path))
    assert not tree


def test_parse_item_with_empty_linked_file(tmp_path):
    """Test parsing an item with a link to an empty XML file."""
    empty_file = tmp_path / "empty.xml"
    empty_file.write_text("<cpc-scheme/>")
    xml_string = f"""
    <classification-item link-file="{empty_file.name}">
        <classification-symbol>A</classification-symbol>
    </classification-item>
    """
    element = ET.fromstring(xml_string)
    parsed = parse_item(element, str(tmp_path))
    assert "children" not in parsed


def test_parse_item_with_no_symbol_in_linked_file(tmp_path):
    """Test parsing an item with a linked file where a sub-item has no symbol."""
    linked_xml_content = """
    <cpc-scheme>
        <classification-item>
            <classification-item>
                <class-title>
                    <title-part><text>No Symbol</text></title-part>
                </class-title>
            </classification-item>
        </classification-item>
    </cpc-scheme>
    """
    linked_file = tmp_path / "linked.xml"
    linked_file.write_text(linked_xml_content)
    xml_string = f"""
    <classification-item link-file="{linked_file.name}">
        <classification-symbol>A</classification-symbol>
    </classification-item>
    """
    element = ET.fromstring(xml_string)
    parsed = parse_item(element, str(tmp_path))
    assert parsed is not None
