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
LAYOUT = {
    "J1": (25, 30), "D1": (60, 30), "C1": (95, 30),
    "#FLG01": (130, 30), "#FLG02": (150, 30),
    "SW1": (25, 75), "R1": (60, 75), "R3": (95, 75),
    "Q1": (135, 75), "R13": (175, 75), "R5": (210, 75),
    "Q3": (245, 75), "R14": (280, 75), "R6": (315, 75),
    "Q4": (350, 75), "R18": (385, 75), "D2": (385, 97),
    "SW2": (25, 105), "R2": (60, 105), "R4": (95, 105),
    "Q2": (135, 105),
    "SW3": (25, 150), "R21": (60, 150), "R7": (95, 150),
    "Q5": (135, 150), "R15": (175, 150), "R9": (210, 150),
    "Q7": (245, 150), "R16": (280, 150), "R10": (315, 150),
    "Q8": (350, 150), "R19": (385, 150), "D3": (385, 172),
    "SW4": (25, 180), "R22": (60, 180), "R8": (95, 180),
    "Q6": (135, 180),
    "SW5": (25, 230), "R23": (60, 230), "R11": (95, 230),
    "Q9": (135, 230), "R17": (175, 230), "R12": (210, 230),
    "Q10": (250, 230), "R20": (290, 230), "D4": (325, 230),
}


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


    def place(self, lib_id: str, ref: str, value: str, x: float, y: float,
              footprint: str, nets: dict[str, str], *, nc: set[str] = frozenset(),
              unit: int = 1, datasheet: str = "") -> None:
        x, y = LAYOUT.get(ref, (x, y))
        x, y = round(x / 1.27) * 1.27, round(y / 1.27) * 1.27
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
        if ref.startswith('Q'):
            rx, ry, vx, vy = x + 12.7, y - 8.89, x + 12.7, y + 8.89
        else:
            rx, ry, vx, vy = x + 7.62, y - 3.81, x + 7.62, y + 3.81
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
  (uuid "{ROOT_UUID}") (paper "A3")
  (title_block (title "Placa 01 - Portas logicas") (date "2026-10-27")
    (rev "A") (company "PET Engenharia Eletrica UFC"))
  (lib_symbols {' '.join(self.lib.values())})
  (text "AND: series NAND plus inverter and LED driver" (at 80 55 0)
    (effects (font (size 2 2) (thickness 0.3))) (uuid "{uid('text:and')}"))
  (text "OR: parallel NOR plus inverter and LED driver" (at 80 130 0)
    (effects (font (size 2 2) (thickness 0.3))) (uuid "{uid('text:or')}"))
  (text "NOT: common-emitter inverter and LED driver" (at 80 210 0)
    (effects (font (size 2 2) (thickness 0.3))) (uuid "{uid('text:not')}"))
  {' '.join(self.items)}
)\n'''
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(content, encoding="utf-8")
        print(f"Wrote {OUT}")


def build() -> Schematic:
    s = Schematic()
    ids = {
        "R": s.add_library("Device", "R"),
        "LED": s.add_library("Device", "LED"),
        "Dsch": s.add_library("Device", "D_Schottky"),
        "SW": s.add_library("Switch", "SW_Push"),
        "J": s.add_library("Connector_Generic", "Conn_01x02"),
        "FLAG": s.add_library("power", "PWR_FLAG"),
        "Q": s.add_library("Transistor_BJT", "Q_NPN_EBC"),
        "C": s.add_library("Device", "C"),
    }
    transistor = "Package_TO_SOT_THT:TO-92_Inline"
    resistor = "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal"
    transistor_datasheet = "https://www.onsemi.com/pdf/datasheet/2n3904-d.pdf"
    led_datasheet = "https://www.vishay.com/docs/83011/tlhr5200.pdf"

    # Protected regulated 5 V input and five independent active-high buttons.
    s.place(ids["J"], "J1", "5V INPUT", 35.56, 35.56,
            "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical",
            {"1": "5V_IN", "2": "GND"})
    s.place(ids["Dsch"], "D1", "1N5819", 53.34, 35.56,
            "Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal",
            {"2": "5V_IN", "1": "VCC"}, datasheet="https://www.diodes.com/datasheet/download/1N5819.pdf")
    s.place(ids["FLAG"], "#FLG01", "PWR_FLAG", 73.66, 35.56, "", {"1": "VCC"})
    s.place(ids["FLAG"], "#FLG02", "PWR_FLAG", 81.28, 35.56, "", {"1": "GND"})
    s.place(ids["C"], "C1", "100nF 50V", 88.9, 35.56,
            "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P2.50mm",
            {"1": "VCC", "2": "GND"})

    switch_datasheet = "https://components.omron.com/us-en/datasheet_pdf/A070-E1.pdf"
    inputs = (("SW1", "A_AND", 60.96), ("SW2", "B_AND", 83.82),
              ("SW3", "A_OR", 106.68), ("SW4", "B_OR", 129.54),
              ("SW5", "A_NOT", 152.4))
    for ref, signal, y in inputs:
        s.place(ids["SW"], ref, "B3F-4050", 40.64, y,
                "Button_Switch_THT:SW_SPST_Omron_B3F-50xx",
                {"1": "VCC", "2": signal}, datasheet=switch_datasheet)
    for ref, signal, y in zip(("R1", "R2", "R21", "R22", "R23"),
                              (item[1] for item in inputs),
                              (item[2] for item in inputs)):
        s.place(ids["R"], ref, "10k 5%", 68.58, y, resistor,
                {"1": signal, "2": "GND"})

    # Base resistors for the two-transistor AND/NAND stack, parallel NOR
    # network, output inverters, and low-side LED indicator drivers.
    base_resistors = [
        ("R3", "A_AND", "Q1_B"), ("R4", "B_AND", "Q2_B"),
        ("R5", "N_AND", "Q3_B"), ("R6", "Y_AND", "Q4_B"),
        ("R7", "A_OR", "Q5_B"), ("R8", "B_OR", "Q6_B"),
        ("R9", "N_OR", "Q7_B"), ("R10", "Y_OR", "Q8_B"),
        ("R11", "A_NOT", "Q9_B"), ("R12", "Y_NOT", "Q10_B"),
    ]
    for index, (ref, source, base) in enumerate(base_resistors):
        x = 88.9 + (index // 5) * 55.88
        y = 53.34 + (index % 5) * 12.7
        s.place(ids["R"], ref, "10k 5%", x, y, resistor,
                {"1": source, "2": base})

    # 2.2 kOhm pull-ups keep HIGH above 3.6 V despite the next 10 kOhm base load.
    pullups = [
        ("R13", "VCC", "N_AND"), ("R14", "VCC", "Y_AND"),
        ("R15", "VCC", "N_OR"), ("R16", "VCC", "Y_OR"),
        ("R17", "VCC", "Y_NOT"),
    ]
    for index, (ref, source, destination) in enumerate(pullups):
        s.place(ids["R"], ref, "2.2k 5%", 152.4, 53.34 + index * 12.7,
                resistor, {"1": source, "2": destination})

    # AND: Q1 and Q2 make a series path to ground when both A and B are high.
    # The N_AND node is NAND; Q3 inverts it to Y_AND. Q4 drives LED D2.
    bjt = lambda ref, base, collector, emitter, x, y: s.place(
        ids["Q"], ref, "2N3904", x, y, transistor,
        {"1": emitter, "2": base, "3": collector}, datasheet=transistor_datasheet
    )
    bjt("Q1", "Q1_B", "N_AND", "N_AND_MID", 116.84, 60.96)
    bjt("Q2", "Q2_B", "N_AND_MID", "GND", 116.84, 83.82)
    bjt("Q3", "Q3_B", "Y_AND", "GND", 137.16, 60.96)
    bjt("Q4", "Q4_B", "LED_AND_K", "GND", 137.16, 83.82)

    # OR: Q5 and Q6 form a parallel NOR pull-down network. Q7 inverts NOR;
    # Q8 is the LED driver for the resulting OR output.
    bjt("Q5", "Q5_B", "N_OR", "GND", 172.72, 60.96)
    bjt("Q6", "Q6_B", "N_OR", "GND", 172.72, 83.82)
    bjt("Q7", "Q7_B", "Y_OR", "GND", 193.04, 60.96)
    bjt("Q8", "Q8_B", "LED_OR_K", "GND", 193.04, 83.82)

    # NOT: Q9 common-emitter inverter and Q10 low-side LED driver.
    bjt("Q9", "Q9_B", "Y_NOT", "GND", 213.36, 60.96)
    bjt("Q10", "Q10_B", "LED_NOT_K", "GND", 213.36, 83.82)

    # Each red LED has an independent 1.5 kOhm series current limiter.
    led_parts = [
        ("R18", "D2", "LED_AND_K", "LED_AND_A", "D2", 137.16, 104.14),
        ("R19", "D3", "LED_OR_K", "LED_OR_A", "D3", 193.04, 104.14),
        ("R20", "D4", "LED_NOT_K", "LED_NOT_A", "D4", 213.36, 104.14),
    ]
    for resistor_ref, led_ref, cathode, anode, value_ref, x, y in led_parts:
        s.place(ids["R"], resistor_ref, "1.5k 5%", x, y, resistor,
                {"1": "VCC", "2": anode})
        s.place(ids["LED"], led_ref, "TLHR5200", x, y + 12.7,
                "LED_THT:LED_D5.0mm", {"2": anode, "1": cathode},
                datasheet=led_datasheet)
    return s


if __name__ == "__main__":
    build().write()
