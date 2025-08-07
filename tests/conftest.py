import pytest


@pytest.fixture
def temp_xml_dir(tmp_path):
    """Create a temporary directory with mock CPC XML files for testing."""
    # Main CPC scheme file
    cpc_scheme_content = """
<cpc-scheme>
    <classification-item>
        <classification-symbol>A</classification-symbol>
        <class-title>
            <title-part><text>HUMAN NECESSITIES</text></title-part>
        </class-title>
        <classification-item>
            <classification-symbol>A01</classification-symbol>
            <class-title>
                <title-part><text>AGRICULTURE</text></title-part>
            </class-title>
            <classification-item>
                <classification-symbol>A01B</classification-symbol>
                <class-title>
                    <title-part><text>SOIL WORKING</text></title-part>
                </class-title>
            </classification-item>
        </classification-item>
    </classification-item>
    <classification-item>
        <classification-symbol>B</classification-symbol>
        <class-title>
            <title-part><text>PERFORMING OPERATIONS</text></title-part>
        </class-title>
        <classification-item link-file="B01.xml">
            <classification-symbol>B01</classification-symbol>
        </classification-item>
    </classification-item>
</cpc-scheme>
"""
    (tmp_path / "cpc-scheme.xml").write_text(cpc_scheme_content)

    # Linked file for B01
    b01_content = """
<classification-item>
    <classification-symbol>B01</classification-symbol>
    <class-title>
        <title-part><text>PHYSICAL OR CHEMICAL PROCESSES</text></title-part>
    </class-title>
    <classification-item>
        <classification-symbol>B01D</classification-symbol>
        <class-title>
            <title-part><text>SEPARATION</text></title-part>
        </class-title>
    </classification-item>
</classification-item>
"""
    (tmp_path / "B01.xml").write_text(b01_content)

    # Malformed XML file
    (tmp_path / "malformed.xml").write_text("<root><unclosed-tag></root>")

    return tmp_path
