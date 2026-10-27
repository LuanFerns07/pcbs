#!/usr/bin/env python3
"""Check the first board's required component-to-net pin mappings."""

from __future__ import annotations

import re
import subprocess
import tempfile
from pathlib import Path


BOARD = Path(__file__).resolve().parents[1] / "boards" / "01-logic-gates"
SCHEMATIC = BOARD / "01-logic-gates.kicad_sch"


def sexp_block(text: str, start: int) -> str:
    depth = 0
    quoted = escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise ValueError("unbalanced KiCad netlist")


def get_nets(netlist: str) -> dict[tuple[str, str], str]:
    result: dict[tuple[str, str], str] = {}
    for match in re.finditer(r"\(net\s+\(code\s+", netlist):
        block = sexp_block(netlist, match.start())
        net_name = re.search(r'\(name\s+"([^"]+)"', block)
        if not net_name:
            continue
        for node in re.finditer(
            r'\(node\s+\(ref\s+"([^"]+)"\)\s+\(pin\s+"([^"]+)"\)', block
        ):
            result[(node.group(1), node.group(2))] = net_name.group(1)
    return result


def verify(actual: dict[tuple[str, str], str]) -> list[str]:
    expected = {
        ("J1", "1"): "/5V_IN", ("J1", "2"): "/GND",
        ("D4", "2"): "/5V_IN", ("D4", "1"): "/VCC",
        ("SW1", "1"): "/VCC", ("SW1", "2"): "/A",
        ("SW2", "1"): "/VCC", ("SW2", "2"): "/B",
        ("R1", "1"): "/A", ("R1", "2"): "/GND",
        ("R2", "1"): "/B", ("R2", "2"): "/GND",
        ("U1", "1"): "/A", ("U1", "2"): "/B", ("U1", "3"): "/Y_AND",
        ("U2", "1"): "/A", ("U2", "2"): "/B", ("U2", "3"): "/Y_OR",
        ("U3", "1"): "/A", ("U3", "2"): "/Y_NOT",
    }
    for ref in ("U1", "U2"):
        for pin in ("4", "5", "7", "9", "10", "12", "13"):
            expected[(ref, pin)] = "/GND"
    for pin in ("3", "5", "7", "9", "11", "13"):
        expected[("U3", pin)] = "/GND"
    for ref in ("U1", "U2", "U3"):
        expected[(ref, "14")] = "/VCC"

    for index, output in enumerate(("Y_AND", "Y_OR", "Y_NOT"), 1):
        expected[(f"R{index + 2}", "1")] = f"/{output}"
        expected[(f"R{index + 2}", "2")] = f"/LED{index}_A"
        expected[(f"D{index}", "2")] = f"/LED{index}_A"
        expected[(f"D{index}", "1")] = "/GND"
        expected[(f"C{index}", "1")] = "/VCC"
        expected[(f"C{index}", "2")] = "/GND"

    errors = [
        f"{ref}.{pin}: expected {net}, got {actual.get((ref, pin), '<unconnected>')}"
        for (ref, pin), net in expected.items()
        if actual.get((ref, pin)) != net
    ]
    unused_outputs = (
        ("U1", "6"), ("U1", "8"), ("U1", "11"),
        ("U2", "6"), ("U2", "8"), ("U2", "11"),
        ("U3", "4"), ("U3", "6"), ("U3", "8"), ("U3", "10"), ("U3", "12"),
    )
    for ref, pin in unused_outputs:
        net = actual.get((ref, pin), "")
        if not net.startswith("unconnected-"):
            errors.append(f"{ref}.{pin}: expected explicit no-connect, got {net or '<unconnected>'}")
    return errors

def main() -> int:
    with tempfile.TemporaryDirectory(prefix="pet-logic-netlist-") as temp_dir:
        output = Path(temp_dir) / "logic-gates.net"
        command = ["kicad-cli", "sch", "export", "netlist", str(SCHEMATIC), "--output", str(output)]
        run = subprocess.run(command, capture_output=True, text=True, check=False)
        if run.returncode:
            print(run.stderr, end="")
            return run.returncode
        errors = verify(get_nets(output.read_text(encoding="utf-8")))
    if errors:
        print("Netlist connectivity check failed:")
        print("\n".join(f"- {message}" for message in errors))
        return 1
    print("Netlist connectivity verified: inputs, logic outputs, unused gates, power and decoupling.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
