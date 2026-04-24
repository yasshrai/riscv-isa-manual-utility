# RISC-V Instruction Parser & Extension Analyzer

This project is a Python-based analysis tool for exploring RISC-V instructions and their associated extensions. It reads from a JSON dictionary of instructions (`instr_dict.json`) and compares the instruction extensions present in the dictionary against those mentioned in the RISC-V ISA manual's source files.

## Features

The assignment is divided into two primary execution tiers:

* **Tier 1 (Data Extraction & Summarization):**
  * Loads RISC-V instructions and their encodings, masks, and variables from `instr_dict.json`.
  * Groups instructions by their architectural extension (e.g., `I`, `M`, `F`, `Zicsr`).
  * Prints a formatted summary of extensions, the number of instructions in each, and an example instruction.
  * Identifies and lists instructions that belong to multiple extensions.

* **Tier 2 (Manual vs. Dictionary Comparison):**
  * Normalizes the extensions extracted from the JSON dictionary (removing prefixes like `rv_`, `rv32_` and standardizing capitalization).
  * Parses the raw source files of the RISC-V ISA manual (located in `riscv-isa-manual/src`) using regular expressions to extract mentioned extensions.
  * Compares the normalized JSON extensions with those found in the manual.
  * Outputs the extensions that match, those only present in the JSON, and those only present in the manual source.

## Project Structure

* `main.py` - Contains the core logic for processing JSON data, parsing the manual files, and the tier execution entries.
* `test_main.py` - Contains `pytest` unit tests for validating the functionality of the functions in `main.py`.
* `instr_dict.json` - The JSON dataset containing RISC-V instructions and their attributes (encoding, match, mask, extensions).
* `riscv-isa-manual/src/` - Directory containing the raw source files of the RISC-V ISA manual.
* `pyproject.toml` / `uv.lock` - Dependency management files specifying `pytest` for testing.

## Setup and Installation

1. Ensure you have Python 3.14+ installed (as specified in `pyproject.toml`).
2. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
3. Install the necessary dependencies:
   ```bash
   uv pip install -e .
   # or alternatively if using pip
   pip install pytest
   ```

## Usage

Run the main script to see the tier 1 and tier 2 output:

```bash
python main.py
```

## Testing

The project uses `pytest` for testing the main functionalities and data transformations.

To run the test suite:

```bash
pytest test_main.py
```