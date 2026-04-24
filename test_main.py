import pytest
import json
from unittest.mock import mock_open, patch

from main import (
    Instruction,
    fetch_instructions,
    group_instruction_by_extension,
    find_multi_extensions_instructions,
    normalize_ext,
    extract_json_extensions,
    compare_extensions,
    extract_manual_extensions,
)

# -------------------------
# Sample JSON test data
# -------------------------
SAMPLE_JSON = {
    "ADD": {
        "encoding": "R",
        "variable_fields": ["rd", "rs1", "rs2"],
        "extension": ["I"],
        "match": "0x33",
        "mask": "0xfe00707f"
    },
    "MUL": {
        "encoding": "R",
        "variable_fields": ["rd", "rs1", "rs2"],
        "extension": ["M"],
        "match": "0x2000033",
        "mask": "0xfe00707f"
    },
    "FMADD": {
        "encoding": "R4",
        "variable_fields": ["rd", "rs1", "rs2", "rs3"],
        "extension": ["F", "D"],
        "match": "0x43",
        "mask": "0x6000007f"
    }
}

# -------------------------
# fetch_instructions
# -------------------------
@patch("builtins.open", new_callable=mock_open, read_data=json.dumps(SAMPLE_JSON))
def test_fetch_instructions(mock_file):
    """
    Tests if instructions are correctly loaded from a JSON file and parsed into
    Instruction objects. Mocks the built-in 'open' function to return SAMPLE_JSON.
    """
    instructions = fetch_instructions("dummy.json")

    assert len(instructions) == 3
    assert isinstance(instructions["ADD"], Instruction)
    assert instructions["ADD"].match == int("0x33", 16)


# -------------------------
# group_instruction_by_extension
# -------------------------
def test_group_instruction_by_extension():
    """
    Tests the grouping logic of instructions by their respective extensions.
    Verifies that the resulting dictionary contains the correct extensions and maps
    them to the appropriate instruction names.
    """
    instructions = {
        k: Instruction(**{
            "encoding": v["encoding"],
            "variable_fields": v["variable_fields"],
            "extension": v["extension"],
            "match": int(v["match"], 16),
            "mask": int(v["mask"], 16),
        })
        for k, v in SAMPLE_JSON.items()
    }

    grouped = group_instruction_by_extension(instructions)

    assert "I" in grouped
    assert "M" in grouped
    assert "F" in grouped
    assert "D" in grouped
    assert "ADD" in grouped["I"]


# -------------------------
# find_multi_extensions_instructions
# -------------------------
def test_find_multi_extensions_instructions():
    """
    Tests the identification of instructions that belong to multiple extensions.
    Verifies that 'FMADD' is correctly identified as belonging to ['F', 'D'].
    """
    instructions = {
        k: Instruction(**{
            "encoding": v["encoding"],
            "variable_fields": v["variable_fields"],
            "extension": v["extension"],
            "match": int(v["match"], 16),
            "mask": int(v["mask"], 16),
        })
        for k, v in SAMPLE_JSON.items()
    }

    multi = find_multi_extensions_instructions(instructions)

    assert len(multi) == 1
    assert multi[0][0] == "FMADD"


# -------------------------
# normalize_ext
# -------------------------
@pytest.mark.parametrize("input_ext,expected", [
    ("rv64_i", "I"),
    ("rv32_m", "M"),
    ("rv_zba", "Zba"),
    ("F", "F"),
])
def test_normalize_ext(input_ext, expected):
    """
    Tests the normalization of extension names with various inputs, ensuring
    prefixes are removed and capitalization is consistent.
    """
    assert normalize_ext(input_ext) == expected


# -------------------------
# extract_json_extensions
# -------------------------
def test_extract_json_extensions():
    """
    Tests the extraction and normalization of extensions directly from
    the grouped JSON instruction data.
    """
    extension_group = {
        "rv64_i": ["ADD"],
        "rv64_m": ["MUL"],
        "rv_zba": ["XYZ"]
    }

    result = extract_json_extensions(extension_group)

    assert result == {"I", "M", "Zba"}


# -------------------------
# compare_extensions
# -------------------------
def test_compare_extensions():
    """
    Tests the comparison logic between extensions extracted from the JSON
    and those parsed from the manual, validating the 'matched', 'json_only',
    and 'manual_only' sets.
    """
    json_exts = {"I", "M", "F"}
    manual_exts = {"M", "F", "D"}

    matched, json_only, manual_only = compare_extensions(json_exts, manual_exts)

    assert matched == {"M", "F"}
    assert json_only == {"I"}
    assert manual_only == {"D"}

# -------------------------
# extract_manual_extensions
# -------------------------
def test_extract_manual_extensions(tmp_path):
    """
    Tests the extraction of RISC-V extensions from filenames using a temporary directory.
    Verifies that it correctly matches Z extensions, single letter extensions, and combined
    RV extensions while ignoring image extensions or non-adoc/tex files.
    """
    # Create mock manual files
    files_to_create = [
        "zicsr.adoc",       # Z extension
        "rv32imafd.tex",    # Combined RV
        "rv64g.adoc",       # Combined RV with 'g'
        "v-st-ext.adoc",    # Single letter 'v'
        "c-ci.edn",         # Image file (should be ignored)
        "intro.adoc"        # Random doc (no extension)
    ]
    
    for filename in files_to_create:
        (tmp_path / filename).touch()
        
    extracted = extract_manual_extensions(str(tmp_path))
    
    # Check that the extensions are normalized and accurately extracted
    assert "Zicsr" in extracted
    assert "I" in extracted
    assert "M" in extracted
    assert "A" in extracted
    assert "F" in extracted
    assert "D" in extracted
    assert "G" in extracted
    assert "V" in extracted
    
    # Should ignore the .edn image file
    assert "C" not in extracted
    
    # Should ignore 'i', 'n', 't', 'r', 'o' from intro.adoc
    assert "R" not in extracted