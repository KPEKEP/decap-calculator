import math
from typing import Union

def format_capacitance(capacitance: float) -> str:
    """Format capacitance in appropriate units"""
    if capacitance >= 1e-3:
        return f"{capacitance*1e3:.2f} mF"
    elif capacitance >= 1e-6:
        return f"{capacitance*1e6:.2f} µF"
    elif capacitance >= 1e-9:
        return f"{capacitance*1e9:.2f} nF"
    else:
        return f"{capacitance*1e12:.2f} pF"

def format_frequency(freq: float) -> str:
    """Format frequency in appropriate units"""
    if freq >= 1e9:
        return f"{freq/1e9:.2f} GHz"
    elif freq >= 1e6:
        return f"{freq/1e6:.2f} MHz"
    elif freq >= 1e3:
        return f"{freq/1e3:.2f} kHz"
    else:
        return f"{freq:.2f} Hz"

def format_impedance(impedance: float) -> str:
    """Format impedance in appropriate units"""
    if impedance >= 1e6:
        return f"{impedance/1e6:.2f} MΩ"
    elif impedance >= 1e3:
        return f"{impedance/1e3:.2f} kΩ"
    else:
        return f"{impedance:.2f} Ω" 