import json
from dataclasses import dataclass
from collections import defaultdict
from typing import List
import os
import re

FILE_PATH = "instr_dict.json"

@dataclass
class Instruction:
    """
    Data class representing a RISC-V instruction.
    Contains attributes for the instruction's encoding format, variable fields (e.g., rd, rs1),
    supported extensions, match bits, and mask bits for decoding.
    """
    encoding:str
    variable_fields:List[str]
    extension:List[str]
    match:str
    mask:str
    
    
def fetch_instructions(file_path:str)->dict:
    """
    Reads instruction data from a JSON file and parses it into Instruction objects.
    Converts hexadecimal string values for 'match' and 'mask' into integers.
    
    Args:
        file_path (str): The path to the JSON file containing instruction data.
        
    Returns:
        dict: A dictionary mapping instruction names to Instruction objects.
    """
    with open(file_path,"r") as f:
        data:dict = json.load(f) 
        instructions = {}
        for instruction_name,instruction_data in data.items():
            instructions[instruction_name] = Instruction(
                encoding=instruction_data["encoding"],
                variable_fields=instruction_data["variable_fields"],
                extension=instruction_data["extension"],
                match=int(instruction_data["match"], 16),
                mask=int(instruction_data["mask"], 16),
            )
    return instructions

def group_instruction_by_extension(instructions:dict)->defaultdict:
    """
    Groups a dictionary of Instructions based on their associated architectural extensions.
    
    Args:
        instructions (dict): A dictionary mapping instruction names to Instruction objects.
        
    Returns:
        defaultdict: A dictionary mapping an extension name to a list of instruction names.
    """
    extensions_groups = defaultdict(list)
    for name,instr in instructions.items():
        for exten in instr.extension:
            extensions_groups[exten].append(name)
    
    return extensions_groups
            
            
def print_summary(extension_group):
    """
    Prints a formatted table summarizing the number of instructions per extension
    and provides an example instruction for each.
    
    Args:
        extension_group (defaultdict): A dictionary grouping instruction names by extension.
    """
    print(f"{'Extension':<15} {'Count':<10} Example")
    print("-" * 40)
    for exten,instr in extension_group.items():
        print(f"{exten:<15} {len(instr):<10} {instr[0]}")
        
def find_multi_extensions_instructions(instructions:dict)->list:
    """
    Finds all instructions that belong to more than one extension.
    
    Args:
        instructions (dict): A dictionary mapping instruction names to Instruction objects.
        
    Returns:
        list: A list of tuples containing (instruction_name, [extensions]).
    """
    multi = []
    for name,instruction in instructions.items():
        if len(instruction.extension) > 1:
            multi.append((name,instruction.extension))
    return multi

def tier1():
    """
    Executes Tier 1 logic: Fetches instructions from the JSON file, groups them by
    their extensions, prints a summary, and lists instructions present in multiple extensions.
    """
    instructions = fetch_instructions(FILE_PATH)
    extension_group = group_instruction_by_extension(instructions)
    print_summary(extension_group)
    multi = find_multi_extensions_instructions(instructions)

    print("\nInstructions in multiple extensions:")
    for name, exts in multi:
        print(f"{name}: {', '.join(exts)}")
    
    

def normalize_ext(ext)->str:
    """
    Normalizes extension names by removing common prefixes and capitalizing the first letter.
    This ensures standardized extension names for accurate comparison.
    
    Args:
        ext (str): The raw extension string.
        
    Returns:
        str: The normalized extension string.
    """
    ext = ext.lower()

    # remove prefixes like rv_, rv64_, etc.
    ext = ext.replace("rv64_", "").replace("rv32_", "").replace("rv_", "")

    # uppercase first letter (Zba, M, F, etc.)
    return ext.capitalize()

def extract_manual_extensions(src_dir) -> set:
    """
    Traverses the manual source directory and extracts RISC-V extensions purely from 
    the filenames, checking if an extension name is present in the file's name.
    
    This uses regular expressions to find substrings in filenames that match 
    known RISC-V extension patterns (Z-extensions, RV-combined extensions, 
    and standalone single-letter extensions). It does not parse file contents.

    Args:
        src_dir (str): The path to the directory containing the RISC-V ISA manual source files.

    Returns:
        set: A set of normalized extension strings found in the filenames.
    """
    found = set()

    for root, _, files in os.walk(src_dir):
        for file in files:
            name = file.lower()

            # Only process doc/tex files to avoid image name false positives
            if not (name.endswith('.adoc') or name.endswith('.tex')):
                continue

            # Remove file extension for cleaner matching
            name = os.path.splitext(name)[0]

            # --- Z extensions (zicsr, zba, etc.) ---
            z_matches = re.findall(r'\bz[a-z0-9]+\b', name)
            for z in z_matches:
                found.add(normalize_ext(z))

            # --- RV combined extensions (rv32imafd etc.) ---
            rv_matches = re.findall(r'rv\d+([imafdbqcegvhsu]+)', name)
            for group in rv_matches:
                for ch in group:
                    found.add(normalize_ext(ch))

            # --- Single letter standalone (rare but safe) ---
            single_matches = re.findall(r'\b([imafdqcebgvhsu])\b', name)
            for s in single_matches:
                found.add(normalize_ext(s))

    return found

def extract_json_extensions(extension_group)->set:
    """
    Extracts and normalizes all unique extensions present in the parsed JSON data.
    
    Args:
        extension_group (defaultdict): Grouped extensions from the JSON file.
        
    Returns:
        set: A set of normalized extension names.
    """
    return {normalize_ext(ext) for ext in extension_group.keys()}

def compare_extensions(json_exts:set, manual_exts:set)->tuple:
    """
    Compares the extensions extracted from the JSON file against those from the manual.
    
    Args:
        json_exts (set): Set of extensions from the JSON file.
        manual_exts (set): Set of extensions parsed from the manual.
        
    Returns:
        tuple: (matched_extensions, json_only_extensions, manual_only_extensions)
    """
    matched =  json_exts.intersection(manual_exts)
    json_only = json_exts.difference(manual_exts)
    manual_only = manual_exts.difference(json_exts)

    return (matched, json_only, manual_only)

def tier2():
    """
    Executes Tier 2 logic: Compares extensions parsed from the JSON dataset against
    extensions mentioned directly in the RISC-V ISA manual source files, then prints
    the matching and disparate sets.
    """
    instructions = fetch_instructions(FILE_PATH)
    extension_group = group_instruction_by_extension(instructions)

    json_exts = extract_json_extensions(extension_group)
    
    manual_exts = extract_manual_extensions("riscv-isa-manual/src")

    matched, json_only, manual_only = compare_extensions(json_exts, manual_exts)

    print("\nMatched Extensions:")
    print(matched)

    print("\nPresent in JSON but NOT in manual:")
    print(json_only)

    print("\nPresent in manual but NOT in JSON:")
    print(manual_only)

    print("\nSummary:")
    print(f"{len(matched)} matched, {len(json_only)} in JSON only, {len(manual_only)} in manual only")
    
    
if __name__ == "__main__":
    tier1()
    tier2()