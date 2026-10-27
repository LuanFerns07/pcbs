#!/usr/bin/env python3
"""Generate the native KiCad schematic for the first PET logic-gates board.

Requires KiCad's standard symbol libraries. The embedded symbols are copied
from the installed libraries at generation time; no third-party package is
required. Run from any directory with Python 3.
"""

from __future__ import annotations

import re
import uuid
from pathlib import Path


BOARD = Path(__file__).resolve().parents[1] / "boards" / "01-logic-gates"
OUT = BOARD / "01-logic-gates.kicad_sch"
PROJECT = "01-logic-gates"
ROOT_UUID = str(uuid.uuid5(uuid.NAMESPACE_URL, "pet-ufc:01-logic-gates:root"))


def uid(seed: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"pet-ufc:01-logic-gates:{seed}"))


def block_at(text: str, start: int) -> str:
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
            continue
        if char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise ValueError("unbalanced S-expression")


def library_symbol(library: str, name: str) -> str:
    path = Path("/usr/share/kicad/symbols") / f"{library}.kicad_sym"
    text = path.read_text(encoding="utf-8")
    match = re.search(rf'\(symbol\s+"{re.escape(name)}"', text)
    if not match:
        raise FileNotFoundError(f"{name} not found in {path}")
    result = block_at(text, match.start())
    return result.replace(f'(symbol "{name}"', f'(symbol "{library}:{name}"', 1)


def pins(symbol: str) -> list[tuple[str, str, float, float]]:
    """Return (number, name, x, y) pin endpoints from a library symbol."""
    found: list[tuple[str, str, float, float]] = []
    # Library pin blocks have a number/name and a single (at x y angle).
    for match in re.finditer(r"\(pin\s+[^\s()]+\s+[^\s()]+", symbol):
        pin_block = block_at(symbol, match.start())
        at = re.search(r"\(at\s+(-?[0-9.]+)\s+(-?[0-9.]+)\s+", pin_block)
        number = re.search(r'\(number\s+"([^"]+)"', pin_block)
        name = re.search(r'\(name\s+"([^"]*)"', pin_block)
        if at and number and name:
            found.append((number.group(1), name.group(1), float(at.group(1)), float(at.group(2))))
    # Multi-unit symbols can repeat pins in alternate graphical units. This
    # project only uses single-unit standard symbols and generated IC symbols.
    unique: dict[str, tuple[str, str, float, float]] = {}
    for pin in found:
        unique.setdefault(pin[0], pin)
    return list(unique.values())


def quoted(value: str) -> str:
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'


def make_ic_symbol(name: str, logic: str, output_name: str, *, qualified: bool = True) -> str:
    """Build a single-unit 14-pin DIP symbol with the real package pin map."""
    if logic in ("AND", "OR"):
        pin_map = {
            "1": ("1A", "input", -12.7, 17.78), "2": ("1B", "input", -12.7, 12.7),
            "4": ("2A", "input", -12.7, 7.62), "5": ("2B", "input", -12.7, 2.54),
            "9": ("3A", "input", -12.7, -2.54), "10": ("3B", "input", -12.7, -7.62),
            "12": ("4A", "input", -12.7, -12.7), "13": ("4B", "input", -12.7, -17.78),
            "14": ("VCC", "power_in", 12.7, 17.78), "3": ("1Y", "output", 12.7, 12.7),
            "6": ("2Y", "output", 12.7, 7.62), "8": ("3Y", "output", 12.7, 2.54),
            "11": ("4Y", "output", 12.7, -2.54), "7": ("GND", "power_in", 12.7, -7.62),
        }
    else:
        pin_map = {
            "1": ("1A", "input", -12.7, 17.78), "3": ("2A", "input", -12.7, 12.7),
            "5": ("3A", "input", -12.7, 7.62), "9": ("4A", "input", -12.7, 2.54),
            "11": ("5A", "input", -12.7, -2.54), "13": ("6A", "input", -12.7, -7.62),
            "14": ("VCC", "power_in", 12.7, 17.78), "2": ("1Y", "output", 12.7, 12.7),
            "4": ("2Y", "output", 12.7, 7.62), "6": ("3Y", "output", 12.7, 2.54),
            "8": ("4Y", "output", 12.7, -2.54), "10": ("5Y", "output", 12.7, -7.62),
            "12": ("6Y", "output", 12.7, -12.7), "7": ("GND", "power_in", 12.7, -17.78),
        }
    pins_sexp = []
    for number, (pin_name, electrical_type, x, y) in pin_map.items():
        angle = 0 if x < 0 else 180
        pins_sexp.append(
            f'''(pin {electrical_type} line (at {x} {y} {angle}) (length 5.08)
              (name {quoted(pin_name)} (effects (font (size 1.0 1.0))))
              (number {quoted(number)} (effects (font (size 1.0 1.0)))))'''
        )
    library_name = f"PET_Logic:{name}" if qualified else name
    return f'''(symbol {quoted(library_name)}
      (pin_names (offset 0.5)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "U" (at 0 22.86 0) (effects (font (size 1.27 1.27))))
      (property "Value" {quoted(name)} (at 0 -22.86 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "Package_DIP:DIP-14_W7.62mm" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (property "ki_fp_filters" "DIP*W7.62mm*" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol {quoted(name + "_0_1")} (rectangle (start -7.62 20.32) (end 7.62 -20.32)
        (stroke (width 0.254) (type default)) (fill (type background))))
      (symbol {quoted(name + "_1_1")} {' '.join(pins_sexp)})
    )'''


class Schematic:
    def __init__(self) -> None:
        self.lib: dict[str, str] = {}
        self.items: list[str] = []
        self.libpins: dict[str, list[tuple[str, str, float, float]]] = {}
        self.refs: set[str] = set()

    def add_library(self, lib: str, name: str, block: str | None = None) -> str:
        lib_id = f"{lib}:{name}"
        if lib_id not in self.lib:
            block = block or library_symbol(lib, name)
            self.lib[lib_id] = block
            self.libpins[lib_id] = pins(block)
        return lib_id

    def add_ic_library(self, name: str, kind: str, output_name: str) -> str:
        lib_id = f"PET_Logic:{name}"
        block = make_ic_symbol(name, kind, output_name)
        self.lib[lib_id] = block
        self.libpins[lib_id] = pins(block)
        return lib_id

    def place(self, lib_id: str, ref: str, value: str, x: float, y: float,
              footprint: str, nets: dict[str, str], *, nc: set[str] = frozenset(),
              unit: int = 1, datasheet: str = "") -> None:
        if ref in self.refs:
            raise ValueError(f"duplicate reference {ref}")
        self.refs.add(ref)
        component_id = uid(f"symbol:{ref}")
        pin_specs = self.libpins[lib_id]
        known = {p[0] for p in pin_specs}
        if set(nets) | set(nc) != known:
            missing = known - set(nets) - set(nc)
            extra = (set(nets) | set(nc)) - known
            raise ValueError(f"{ref} pin mapping mismatch missing={missing} extra={extra}")
        labels = []
        no_connects = []
        pin_instances = []
        for number, _name, px, py in pin_specs:
            sx, sy = x + px, y - py
            pin_instances.append(f'(pin {quoted(number)} (uuid "{uid(f"{ref}:pin:{number}")}"))')
            if number in nets:
                labels.append(
                    f'''(label {quoted(nets[number])} (at {sx:.4f} {sy:.4f} 0)
                      (effects (font (size 1.0 1.0)) (justify left bottom))
                      (uuid "{uid(f"{ref}:label:{number}")}"))'''
                )
            else:
                no_connects.append(
                    f'''(no_connect (at {sx:.4f} {sy:.4f})
                      (uuid "{uid(f"{ref}:nc:{number}")}"))'''
                )
        # Place ref/value fields to the right except for DIP symbols, whose
        # fields are centered above and below the body.
        if ref.startswith("U"):
            rx, ry, vx, vy = x, y - 24.13, x, y + 24.13
        else:
            rx, ry, vx, vy = x + 5.08, y - 1.27, x + 5.08, y + 1.27
        instance = f'''(symbol (lib_id {quoted(lib_id)}) (at {x} {y} 0) (unit {unit})
          (in_bom yes) (on_board yes) (dnp no) (uuid "{component_id}")
          (property "Reference" {quoted(ref)} (at {rx:.4f} {ry:.4f} 0)
            (effects (font (size 1.27 1.27)) (justify left)))
          (property "Value" {quoted(value)} (at {vx:.4f} {vy:.4f} 0)
            (effects (font (size 1.27 1.27)) (justify left)))
          (property "Footprint" {quoted(footprint)} (at {x} {y} 0)
            (effects (font (size 1.0 1.0)) hide))
          (property "Datasheet" {quoted(datasheet)} (at {x} {y} 0)
            (effects (font (size 1.0 1.0)) hide))
          {' '.join(pin_instances)}
          (instances (project {quoted(PROJECT)} (path "/{ROOT_UUID}"
            (reference {quoted(ref)}) (unit {unit}))))
        )'''
        self.items.append(instance)
        self.items.extend(labels)
        self.items.extend(no_connects)

    def write(self) -> None:
        content = f'''(kicad_sch
  (version 20250114) (generator "eeschema") (generator_version "9.0")
  (uuid "{ROOT_UUID}") (paper "A4")
  (title_block (title "Placa 01 - Portas logicas") (date "2026-10-27")
    (rev "A") (company "PET Engenharia Eletrica UFC"))
  (lib_symbols {' '.join(self.lib.values())})
  {' '.join(self.items)}
)\n'''
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(content, encoding="utf-8")
        (BOARD / f"{PROJECT}.kicad_pro").write_text("{}\n", encoding="utf-8")
        library_dir = BOARD.parents[1] / "libraries" / "symbols"
        library_dir.mkdir(parents=True, exist_ok=True)
        ic_blocks = [make_ic_symbol(name, kind, output, qualified=False) for name, kind, output in (
            ("SN74HC08", "AND", "Y_AND"), ("SN74HC32", "OR", "Y_OR"),
            ("SN74HC04", "NOT", "Y_NOT"),
        )]
        library = '(kicad_symbol_lib (version 20211014) (generator "kicad_symbol_editor")\n' + "\n".join(ic_blocks) + "\n)\n"
        (library_dir / "PET_Logic.kicad_sym").write_text(library, encoding="utf-8")
        table = '''(sym_lib_table
  (version 7)
  (lib (name "PET_Logic") (type "KiCad")
    (uri "${KIPRJMOD}/../../libraries/symbols/PET_Logic.kicad_sym")
    (options "") (descr "PET UFC educational logic IC symbols"))
)
'''
        (BOARD / "sym-lib-table").write_text(table, encoding="utf-8")
        print(f"Wrote {OUT}")


def build() -> Schematic:
    s = Schematic()
    ids = {
        "R": s.add_library("Device", "R"),
        "C": s.add_library("Device", "C"),
        "LED": s.add_library("Device", "LED"),
        "Dsch": s.add_library("Device", "D_Schottky"),
        "SW": s.add_library("Switch", "SW_Push"),
        "J": s.add_library("Connector_Generic", "Conn_01x02"),
        "FLAG": s.add_library("power", "PWR_FLAG"),
    }
    u_and = s.add_ic_library("SN74HC08", "AND", "Y_AND")
    u_or = s.add_ic_library("SN74HC32", "OR", "Y_OR")
    u_not = s.add_ic_library("SN74HC04", "NOT", "Y_NOT")

    # Low-voltage input, series reverse-polarity protection, and power flags.
    s.place(ids["J"], "J1", "5V INPUT", 45.72, 45.72,
            "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical",
            {"1": "5V_IN", "2": "GND"})
    s.place(ids["Dsch"], "D4", "1N5819", 66.04, 45.72,
            "Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal",
            {"2": "5V_IN", "1": "VCC"}, datasheet="https://www.diodes.com/datasheet/download/1N5819.pdf")
    s.place(ids["FLAG"], "#FLG01", "PWR_FLAG", 83.82, 45.72, "", {"1": "VCC"})
    s.place(ids["FLAG"], "#FLG02", "PWR_FLAG", 91.44, 45.72, "", {"1": "GND"})

    # Manual inputs: each button pulls an input high; each 10-kohm resistor
    # defines a low level when released.
    switch_datasheet = "https://components.omron.com/us-en/datasheet_pdf/A070-E1.pdf"
    s.place(ids["SW"], "SW1", "B3F-4050", 45.72, 78.74,
            "Button_Switch_THT:SW_SPST_Omron_B3F-50xx", {"1": "VCC", "2": "A"}, datasheet=switch_datasheet)
    s.place(ids["SW"], "SW2", "B3F-4050", 45.72, 101.6,
            "Button_Switch_THT:SW_SPST_Omron_B3F-50xx", {"1": "VCC", "2": "B"}, datasheet=switch_datasheet)
    resistor = "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal"
    for ref, net, y in (("R1", "A", 78.74), ("R2", "B", 101.6)):
        s.place(ids["R"], ref, "10k 5%", 76.2, y, resistor, {"1": net, "2": "GND"})

    # Three independent, buffered-by-the-logic outputs. Each red LED is
    # individually current limited with a 1.5-kohm series resistor.
    ic_footprint = "Package_DIP:DIP-14_W7.62mm"
    s.place(u_and, "U1", "SN74HC08N", 109.22, 50.8, ic_footprint,
            {"1": "A", "2": "B", "3": "Y_AND", "4": "GND", "5": "GND",
             "7": "GND", "9": "GND", "10": "GND", "12": "GND", "13": "GND", "14": "VCC"},
            nc={"6", "8", "11"}, datasheet="https://www.ti.com/lit/ds/symlink/sn74hc08.pdf")
    s.place(u_or, "U2", "SN74HC32N", 109.22, 101.6, ic_footprint,
            {"1": "A", "2": "B", "3": "Y_OR", "4": "GND", "5": "GND",
             "7": "GND", "9": "GND", "10": "GND", "12": "GND", "13": "GND", "14": "VCC"},
            nc={"6", "8", "11"}, datasheet="https://www.ti.com/lit/ds/symlink/sn74hc32.pdf")
    s.place(u_not, "U3", "SN74HC04N", 109.22, 152.4, ic_footprint,
            {"1": "A", "2": "Y_NOT", "3": "GND", "5": "GND", "7": "GND",
             "9": "GND", "11": "GND", "13": "GND", "14": "VCC"},
            nc={"4", "6", "8", "10", "12"}, datasheet="https://www.ti.com/lit/ds/symlink/sn74hc04.pdf")

    led_footprint = "LED_THT:LED_D5.0mm"
    for index, (net, y) in enumerate((("Y_AND", 50.8), ("Y_OR", 101.6), ("Y_NOT", 152.4)), 1):
        rref, dref = f"R{index + 2}", f"D{index}"
        anode_net = f"LED{index}_A"
        s.place(ids["R"], rref, "1.5k 5%", 162.56, y, resistor,
                {"1": net, "2": anode_net})
        s.place(ids["LED"], dref, "TLHR5200", 182.88, y, led_footprint,
                {"2": anode_net, "1": "GND"}, datasheet="https://www.vishay.com/docs/83011/tlhr5200.pdf")

    cap_footprint = "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P2.50mm"
    for index, y in enumerate((50.8, 101.6, 152.4), 1):
        s.place(ids["C"], f"C{index}", "100nF 50V", 139.7, y, cap_footprint,
                {"1": "VCC", "2": "GND"})
    return s


if __name__ == "__main__":
    build().write()
