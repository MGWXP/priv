import sys, yaml, pathlib

DOC = pathlib.Path("docs/custom-instructions.md")
REG = pathlib.Path("prompt-registry.yaml")

if not DOC.exists():
    sys.exit("ERROR: docs/custom-instructions.md missing")

reg = yaml.safe_load(REG.read_text())
if "custom_instructions" not in reg:
    reg["custom_instructions"] = {"file": str(DOC), "version": "2025-05-22"}
    REG.write_text(yaml.dump(reg, sort_keys=False))
    print("INFO: Added custom_instructions pointer to prompt-registry.yaml")
