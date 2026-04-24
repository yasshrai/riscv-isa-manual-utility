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
## Sample Output

xtension       Count      Example
----------------------------------------
rv_i            37         add
rv64_zba        5          add_uw
rv64_i          15         addiw
rv32_zknd       2          aes32dsi
rv32_zk         10         aes32dsi
rv32_zkn        10         aes32dsi
rv32_zkne       2          aes32esi
rv64_zknd       5          aes64ds
rv64_zkn        16         aes64ds
rv64_zk         16         aes64ds
rv64_zkne       4          aes64es
rv_zabha        18         amoadd_b
rv64_a          11         amoadd_d
rv_a            11         amoadd_w
rv_zabha_zacas  2          amocas_b
rv_zacas        2          amocas_d
rv64_zacas      1          amocas_q
rv_zbb          17         andn
rv_zkn          15         andn
rv_zks          15         andn
rv_zk           15         andn
rv_zbkb         7          andn
rv_zbs          4          bclr
rv64_zbs        4          bclri
rv_zibi         2          beqi
rv_c            23         c_add
rv64_c          10         c_addiw
rv_c_d          4          c_fld
rv32_c_f        4          c_flw
rv32_c          1          c_jal
rv_zcb          11         c_lbu
rv_zcmop        1          c_mop_N
rv64_zcb        1          c_zext_w
rv_zicbo        4          cbo_clean
rv_zbc          3          clmul
rv_zbkc         2          clmul
rv64_zbb        9          clzw
rv_zcmt         1          cm_jalt
rv_zcmp         6          cm_mva01s
rv_zicsr        6          csrrc
rv_zkr          1          csrrand
rv64_zkr        1          csrrand64
rv_zicond       2          czero_eqz
rv_m            8          div
rv64_m          5          divuw
rv_sdext        1          dret
rv_d            26         fadd_d
rv_zfh          22         fadd_h
rv_q            30         fadd_q
rv_f            26         fadd_s
rv_zfbfmin      2          fcvt_bf16_s
rv_d_zfhmin     2          fcvt_d_h
rv64_d          6          fcvt_d_l
rv64_zfh        4          fcvt_h_l
rv_q_zfhmin     2          fcvt_h_q
rv_zfhmin       6          fcvt_h_s
rv64_q          4          fcvt_l_q
rv64_f          4          fcvt_l_s
rv_d_zfa        8          fcvtmod_w_d
rv_zifencei     1          fence_i
rv_zfh_zfa      7          fleq_h
rv_q_zfa        7          fleq_q
rv_f_zfa        7          fleq_s
rv32_d_zfa      2          fmvh_x_d
rv64_q_zfa      2          fmvh_x_q
rv64_zbp        5          gorci
rv_h            13         hfence_gvma
rv_svinval_h    2          hinval_gvma
rv64_h          3          hlv_d
rv_zalasr       8          lb_aq
rv_smrnmi       1          mnret
rv_zimop        2          mop_r_N
rv_system       2          mret
rv64_zbkb       5          packw
rv64_zks        5          packw
rv_ssctr        1          sctrclr
rv_svinval      3          sfence_inval_ir
rv_s            2          sfence_vma
rv_zba          3          sh1add
rv_zknh         4          sha256sig0
rv64_zknh       4          sha512sig0
rv32_zknh       6          sha512sig0h
rv_zksh         2          sm3p0
rv_zksed        2          sm4ed
rv_zicfiss      2          ssamoswap_d
rv_u            1          uret
rv_v            627        vaadd_vv
rv_zvabd        5          vabd_vv
rv_zvkned       11         vaesdf_vs
rv_zvkn         23         vaesdf_vs
rv_zvbb         16         vandn_vv
rv_zvks         14         vandn_vv
rv_zvbc         4          vclmul_vv
rv_zvfbdot32f   1          vfbdot_vv
rv_zvfofp4min   1          vfext_vf2
rv_zvfofp8min   3          vfncvt_f_f_q
rv_zvfbfmin     2          vfncvtbf16_f_f_w
rv_zvfqbdot8f   2          vfqbdot_alt_vv
rv_zvfqldot8f   2          vfqldot_alt_vv
rv_zvfwbdot16bf 1          vfwbdot_vv
rv_zvfwldot16bf 1          vfwldot_vv
rv_zvfbfwma     2          vfwmaccbf16_vf
rv_zvkg         2          vghsh_vv
rv_zvzip        5          vpaire_vv
rv_zvqbdot8i    2          vqbdots_vv
rv_zvqdotq      7          vqdot_vv
rv_zvqldot8i    2          vqldots_vv
rv_zvknha       3          vsha2ch_vv
rv_zvknhb       3          vsha2ch_vv
rv_zvksh        2          vsm3c_vi
rv_zvksed       3          vsm4k_vi
rv_zawrs        2          wrs_nto
rv_zbp          1          xperm16
rv_zbkx         2          xperm4

Instructions in multiple extensions:
aes32dsi: rv32_zknd, rv32_zk, rv32_zkn
aes32dsmi: rv32_zknd, rv32_zk, rv32_zkn
aes32esi: rv32_zkne, rv32_zk, rv32_zkn
aes32esmi: rv32_zkne, rv32_zk, rv32_zkn
aes64ds: rv64_zknd, rv64_zkn, rv64_zk
aes64dsm: rv64_zknd, rv64_zkn, rv64_zk
aes64es: rv64_zkne, rv64_zkn, rv64_zk
aes64esm: rv64_zkne, rv64_zkn, rv64_zk
aes64im: rv64_zknd, rv64_zkn, rv64_zk
aes64ks1i: rv64_zknd, rv64_zkn, rv64_zkne, rv64_zk
aes64ks2: rv64_zknd, rv64_zkn, rv64_zkne, rv64_zk
andn: rv_zbb, rv_zkn, rv_zks, rv_zk, rv_zbkb
clmul: rv_zbc, rv_zkn, rv_zks, rv_zk, rv_zbkc
clmulh: rv_zbc, rv_zkn, rv_zks, rv_zk, rv_zbkc
orn: rv_zbb, rv_zkn, rv_zks, rv_zk, rv_zbkb
pack: rv_zbkb, rv_zkn, rv_zks, rv_zk
packh: rv_zbkb, rv_zkn, rv_zks, rv_zk
packw: rv64_zbkb, rv64_zks, rv64_zkn, rv64_zk
rol: rv_zbb, rv_zkn, rv_zks, rv_zk, rv_zbkb
rolw: rv64_zbb, rv64_zks, rv64_zkn, rv64_zk, rv64_zbkb
ror: rv_zbb, rv_zkn, rv_zks, rv_zk, rv_zbkb
rori: rv64_zbb, rv64_zks, rv64_zkn, rv64_zk, rv64_zbkb
roriw: rv64_zbb, rv64_zks, rv64_zkn, rv64_zk, rv64_zbkb
rorw: rv64_zbb, rv64_zks, rv64_zkn, rv64_zk, rv64_zbkb
sha256sig0: rv_zknh, rv_zkn, rv_zk
sha256sig1: rv_zknh, rv_zkn, rv_zk
sha256sum0: rv_zknh, rv_zkn, rv_zk
sha256sum1: rv_zknh, rv_zkn, rv_zk
sha512sig0: rv64_zknh, rv64_zkn, rv64_zk
sha512sig0h: rv32_zknh, rv32_zk, rv32_zkn
sha512sig0l: rv32_zknh, rv32_zk, rv32_zkn
sha512sig1: rv64_zknh, rv64_zkn, rv64_zk
sha512sig1h: rv32_zknh, rv32_zk, rv32_zkn
sha512sig1l: rv32_zknh, rv32_zk, rv32_zkn
sha512sum0: rv64_zknh, rv64_zkn, rv64_zk
sha512sum0r: rv32_zknh, rv32_zk, rv32_zkn
sha512sum1: rv64_zknh, rv64_zkn, rv64_zk
sha512sum1r: rv32_zknh, rv32_zk, rv32_zkn
sm3p0: rv_zksh, rv_zks
sm3p1: rv_zksh, rv_zks
sm4ed: rv_zksed, rv_zks
sm4ks: rv_zksed, rv_zks
vaesdf_vs: rv_zvkned, rv_zvkn
vaesdf_vv: rv_zvkned, rv_zvkn
vaesdm_vs: rv_zvkned, rv_zvkn
vaesdm_vv: rv_zvkned, rv_zvkn
vaesef_vs: rv_zvkned, rv_zvkn
vaesef_vv: rv_zvkned, rv_zvkn
vaesem_vs: rv_zvkned, rv_zvkn
vaesem_vv: rv_zvkned, rv_zvkn
vaeskf1_vi: rv_zvkned, rv_zvkn
vaeskf2_vi: rv_zvkned, rv_zvkn
vaesz_vs: rv_zvkned, rv_zvkn
vandn_vv: rv_zvbb, rv_zvks, rv_zvkn
vandn_vx: rv_zvbb, rv_zvks, rv_zvkn
vbrev8_v: rv_zvbb, rv_zvks, rv_zvkn
vrev8_v: rv_zvbb, rv_zvks, rv_zvkn
vrol_vv: rv_zvbb, rv_zvks, rv_zvkn
vrol_vx: rv_zvbb, rv_zvks, rv_zvkn
vror_vi: rv_zvbb, rv_zvks, rv_zvkn
vror_vv: rv_zvbb, rv_zvks, rv_zvkn
vror_vx: rv_zvbb, rv_zvks, rv_zvkn
vsha2ch_vv: rv_zvknha, rv_zvknhb, rv_zvkn
vsha2cl_vv: rv_zvknha, rv_zvknhb, rv_zvkn
vsha2ms_vv: rv_zvknha, rv_zvknhb, rv_zvkn
vsm3c_vi: rv_zvksh, rv_zvks
vsm3me_vv: rv_zvksh, rv_zvks
vsm4k_vi: rv_zvksed, rv_zvks
vsm4r_vs: rv_zvksed, rv_zvks
vsm4r_vv: rv_zvksed, rv_zvks
xnor: rv_zbb, rv_zkn, rv_zks, rv_zk, rv_zbkb
xperm4: rv_zbkx, rv_zkn, rv_zks, rv_zk
xperm8: rv_zbkx, rv_zkn, rv_zks, rv_zk

Matched Extensions:
{'Q', 'Zvfbfwma', 'F', 'M', 'Zimop', 'Zawrs', 'Zcmp', 'Zfh', 'C', 'Zvfbfmin', 'Zacas', 'Zalasr', 'Zicond', 'Zifencei', 'Zfhmin', 'D', 'Zcb', 'A', 'Zabha', 'Zicsr', 'Zcmop', 'Zfbfmin', 'Zcmt', 'V'}

Present in JSON but NOT in manual:
{'Sdext', 'Smrnmi', 'Zvfqbdot8f', 'Q_zfhmin', 'Zvkn', 'Zbkb', 'Zvqldot8i', 'Zvksed', 'Zvfofp8min', 'Zbc', 'S', 'Q_zfa', 'Zvfbdot32f', 'D_zfhmin', 'I', 'Zabha_zacas', 'Zbp', 'Svinval_h', 'Zvfofp4min', 'Zvfwldot16bf', 'Zba', 'System', 'Zvqbdot8i', 'Zvksh', 'Zibi', 'Zbb', 'Zk', 'Zicfiss', 'U', 'Zfh_zfa', 'D_zfa', 'Zksed', 'Zvknha', 'C_d', 'Zbs', 'C_f', 'Zvfqldot8f', 'Ssctr', 'Zksh', 'Zks', 'Zbkx', 'Zicbo', 'Zkn', 'Zknh', 'Zbkc', 'Zvqdotq', 'H', 'Zvkned', 'Zkr', 'Zvks', 'Zvabd', 'Zvknhb', 'Zknd', 'Zvbc', 'Zkne', 'F_zfa', 'Svinval', 'Zvbb', 'Zvzip', 'Zvfwbdot16bf', 'Zvkg'}

Present in manual but NOT in JSON:
{'Zihpm', 'Zpm', 'Ziccamoc', 'Ziccrse', 'Zp', 'Zcd', 'Za', 'Zic64b', 'Zalrsc', 'Zilsd', 'Ziccif', 'Zi', 'Zce', 'Ztso', 'Zihintntl', 'Zclsd', 'Zmmul', 'E', 'Zars', 'Zfa', 'Ziccamoa', 'Zama', 'Zicntr', 'Zihintpause', 'Zca', 'Zicclsm', 'Zc', 'Zfinx', 'Zcf', 'Zaamo', 'B', 'Zf'}

Summary:
24 matched, 61 in JSON only, 32 in manual only