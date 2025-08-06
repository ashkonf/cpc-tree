from cpc_tree import build_cpc_tree, load_cpc_tree


def test_build_cpc_tree():
    """Test building the CPC tree from XML files."""
    cpc_tree = build_cpc_tree("CPCSchemeXML202508")

    # Assertions for top-level 'A'
    assert "A" in cpc_tree
    assert cpc_tree["A"]["title"] == "HUMAN NECESSITIES"
    assert "A01" in cpc_tree["A"]["children"]

    # Check that 'A01' has the correct title and children
    a01 = cpc_tree["A"]["children"]["A01"]
    assert isinstance(a01, dict)
    assert "title" in a01
    assert a01["title"] == "AGRICULTURE"
    assert "children" in a01
    assert "A01" in a01["children"]

    # Check nested 'A01' node
    a01_nested = a01["children"]["A01"]
    assert isinstance(a01_nested, dict)
    assert "title" in a01_nested
    assert a01_nested["title"] == "AGRICULTURE FORESTRY ANIMAL HUSBANDRY HUNTING TRAPPING FISHING"
    assert "children" in a01_nested
    assert "A01B" in a01_nested["children"]

    # Check 'A01B' node
    a01b = a01_nested["children"]["A01B"]
    assert isinstance(a01b, dict)
    assert "title" in a01b
    assert a01b["title"].startswith("SOIL WORKING IN AGRICULTURE OR FORESTRY")
    assert "children" in a01b
    assert "A01B1/00" in a01b["children"]

    # Check a leaf node deep in the tree
    a01b1_00 = a01b["children"]["A01B1/00"]
    assert "children" in a01b1_00
    assert "A01B1/00" in a01b1_00["children"]
    a01b1_00_leaf = a01b1_00["children"]["A01B1/00"]
    assert "title" in a01b1_00_leaf
    assert a01b1_00_leaf["title"].startswith("Hand tools")
    assert "children" in a01b1_00_leaf
    assert "A01B1/02" in a01b1_00_leaf["children"]

    # Check a sub-leaf node
    a01b1_02 = a01b1_00_leaf["children"]["A01B1/02"]
    assert "title" in a01b1_02
    assert a01b1_02["title"].startswith("Spades Shovels")
    assert "children" in a01b1_02
    assert "A01B1/022" in a01b1_02["children"]
    assert "A01B1/024" in a01b1_02["children"]
    assert "A01B1/026" in a01b1_02["children"]
    assert "A01B1/028" in a01b1_02["children"]
    assert "A01B1/04" in a01b1_02["children"]

    # Check a leaf node with a title
    a01b1_04 = a01b1_02["children"]["A01B1/04"]
    assert "title" in a01b1_04
    assert a01b1_04["title"].startswith("with teeth")

def test_load_cpc_tree():
    """Test loading the CPC tree from a dictionary into CPCTreeNode objects."""
    cpc_tree_data = build_cpc_tree("CPCSchemeXML202508")
    cpc_tree = load_cpc_tree(cpc_tree_data)

    # Check root node
    assert "A" in cpc_tree
    root_node = cpc_tree["A"]
    assert root_node.code == "A"
    assert root_node.title == "HUMAN NECESSITIES"
    assert "A01" in root_node.children

    # Check 'A01' node
    a01_node = root_node.children["A01"]
    assert a01_node.code == "A01"
    assert a01_node.title == "AGRICULTURE"

    # Since the structure repeats, we need to go deeper to get the full title
    a01_child_node = a01_node.children["A01"]
    assert a01_child_node.code == "A01"
    assert a01_child_node.title == "AGRICULTURE FORESTRY ANIMAL HUSBANDRY HUNTING TRAPPING FISHING"
    assert "A01B" in a01_child_node.children

    # Check 'A01B' node
    a01b_node = a01_child_node.children["A01B"]
    assert a01b_node.code == "A01B"
    assert a01b_node.title.startswith("SOIL WORKING IN AGRICULTURE OR FORESTRY")
    assert "A01B1/00" in a01b_node.children

    # Check a leaf node deep in the tree
    a01b1_00_node = a01b_node.children["A01B1/00"]
    assert "A01B1/00" in a01b1_00_node.children
    a01b1_00_leaf = a01b1_00_node.children["A01B1/00"]
    assert a01b1_00_leaf.code == "A01B1/00"
    assert a01b1_00_leaf.title.startswith("Hand tools")
    assert "A01B1/02" in a01b1_00_leaf.children

    # Check a sub-leaf node
    a01b1_02_node = a01b1_00_leaf.children["A01B1/02"]
    assert a01b1_02_node.code == "A01B1/02"
    assert a01b1_02_node.title.startswith("Spades Shovels")
    for code in ["A01B1/022", "A01B1/024", "A01B1/026", "A01B1/028", "A01B1/04"]:
        assert code in a01b1_02_node.children

    # Check a leaf node with a title
    a01b1_04_node = a01b1_02_node.children["A01B1/04"]
    assert a01b1_04_node.code == "A01B1/04"
    assert a01b1_04_node.title.startswith("with teeth")
    assert not a01b1_04_node.children


