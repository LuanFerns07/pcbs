#!/usr/bin/env python3
"""Create a preliminary, deterministic two-layer THT layout with pcbnew."""

from __future__ import annotations

import pcbnew
from pathlib import Path


BOARD_DIR = Path(__file__).resolve().parents[1] / "boards" / "01-logic-gates"
PCB_FILE = BOARD_DIR / "01-logic-gates.kicad_pcb"
LIB_DIR = Path("/usr/share/kicad/footprints")


def mm(value: float) -> int:
    return pcbnew.FromMM(value)


def point(x: float, y: float) -> pcbnew.VECTOR2I:
    return pcbnew.VECTOR2I(mm(x), mm(y))


def add_text(board: pcbnew.BOARD, text: str, x: float, y: float, size: float = 1.4) -> None:
    item = pcbnew.PCB_TEXT(board)
    item.SetText(text)
    item.SetPosition(point(x, y))
    item.SetLayer(pcbnew.F_SilkS)
    item.SetTextSize(point(size, size))
    item.SetTextThickness(mm(0.22))
    board.Add(item)


def add_outline(board: pcbnew.BOARD) -> None:
    corners = [(3, 3), (117, 3), (117, 147), (3, 147), (3, 3)]
    for first, second in zip(corners, corners[1:]):
        edge = pcbnew.PCB_SHAPE(board)
        edge.SetShape(pcbnew.SHAPE_T_SEGMENT)
        edge.SetStart(point(*first))
        edge.SetEnd(point(*second))
        edge.SetLayer(pcbnew.Edge_Cuts)
        edge.SetWidth(mm(0.05))
        board.Add(edge)


def load_footprint(board: pcbnew.BOARD, ref: str, value: str, lib_id: str,
                   x: float, y: float, rotation: float, nets: dict[str, str],
                   net_items: dict[str, pcbnew.NETINFO_ITEM]) -> pcbnew.FOOTPRINT:
    library, name = lib_id.split(":", 1)
    footprint = pcbnew.FootprintLoad(str(LIB_DIR / f"{library}.pretty"), name)
    if footprint is None:
        raise FileNotFoundError(f"Footprint not found: {lib_id}")
    footprint.SetReference(ref)
    footprint.SetValue(value)
    footprint.SetFPID(pcbnew.LIB_ID(library, name))
    footprint.SetPosition(point(x, y))
    footprint.SetOrientationDegrees(-rotation)
    footprint.SetPath(pcbnew.KIID_PATH(f"/00000000-0000-0000-0000-{len(board.GetFootprints()) + 1:012d}"))
    for pad in footprint.Pads():
        number = pad.GetNumber()
        if number in nets:
            pad.SetNet(net_items[nets[number]])
    board.Add(footprint)
    return footprint


def main() -> None:
    board = pcbnew.BOARD()
    board.SetCopperLayerCount(2)
    board.SetFileName(str(PCB_FILE))
    design = board.GetDesignSettings()
    design.m_MinClearance = mm(0.25)
    design.m_TrackMinWidth = mm(0.35)
    design.m_ViasMinSize = mm(0.8)
    design.m_ViasMinDrill = mm(0.4)
    design.m_HoleToHoleMin = mm(0.5)

    net_names = ["GND", "VCC", "5V_IN", "A", "B", "Y_AND", "Y_OR", "Y_NOT",
                 "LED1_A", "LED2_A", "LED3_A"]
    nets = {name: pcbnew.NETINFO_ITEM(board, name) for name in net_names}
    for net in nets.values():
        board.Add(net)

    add_outline(board)
    add_text(board, "PET UFC | PORTAS LOGICAS", 18, 12, 2.0)
    add_text(board, "A E B: pressione para nivel alto", 26, 18, 1.5)
    add_text(board, "ENTRADA 5 V REGULADOS", 27, 22)
    add_text(board, "A", 45, 48, 2.0)
    add_text(board, "B", 45, 76, 2.0)
    add_text(board, "AND", 93, 46, 2.0)
    add_text(board, "OR", 93, 76, 2.0)
    add_text(board, "NOT A", 93, 106, 2.0)
    add_text(board, "NAO INVERTER POLARIDADE | FONTE COM LIMITE DE CORRENTE", 28, 139, 1.0)

    footprints = [
        ("J1", "5V INPUT", "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", 20, 27, 0, {"1": "5V_IN", "2": "GND"}),
        ("D4", "1N5819", "Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal", 34, 27, 0, {"1": "VCC", "2": "5V_IN"}),
        ("SW1", "B3F-4050", "Button_Switch_THT:SW_SPST_Omron_B3F-50xx", 47, 55, 0, {"1": "VCC", "2": "A"}),
        ("SW2", "B3F-4050", "Button_Switch_THT:SW_SPST_Omron_B3F-50xx", 47, 83, 0, {"1": "VCC", "2": "B"}),
        ("R1", "10k 5%", "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal", 63, 56, 90, {"1": "A", "2": "GND"}),
        ("R2", "10k 5%", "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal", 63, 84, 90, {"1": "B", "2": "GND"}),
        ("U1", "SN74HC08N", "Package_DIP:DIP-14_W7.62mm", 28, 55, 0, {"1": "A", "2": "B", "3": "Y_AND", "4": "GND", "5": "GND", "7": "GND", "9": "GND", "10": "GND", "12": "GND", "13": "GND", "14": "VCC"}),
        ("U2", "SN74HC32N", "Package_DIP:DIP-14_W7.62mm", 28, 85, 0, {"1": "A", "2": "B", "3": "Y_OR", "4": "GND", "5": "GND", "7": "GND", "9": "GND", "10": "GND", "12": "GND", "13": "GND", "14": "VCC"}),
        ("U3", "SN74HC04N", "Package_DIP:DIP-14_W7.62mm", 28, 115, 0, {"1": "A", "2": "Y_NOT", "3": "GND", "5": "GND", "7": "GND", "9": "GND", "11": "GND", "13": "GND", "14": "VCC"}),
    ]
    for index, (ref, net, y) in enumerate((("R3", "Y_AND", 50), ("R4", "Y_OR", 80), ("R5", "Y_NOT", 110)), 1):
        footprints.extend([
            (ref, "1.5k 5%", "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal", 78, y, 90, {"1": net, "2": f"LED{index}_A"}),
            (f"D{index}", "TLHR5200", "LED_THT:LED_D5.0mm", 98, y, 0, {"1": "GND", "2": f"LED{index}_A"}),
            (f"C{index}", "100nF 50V", "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P2.50mm", 74, y + 15, 90, {"1": "VCC", "2": "GND"}),
        ])
    for args in footprints:
        load_footprint(board, *args, nets)

    # Copper routing and the ground plane remain pending.

    pcbnew.SaveBoard(str(PCB_FILE), board)
    print(f"Wrote {PCB_FILE}")


if __name__ == "__main__":
    main()
