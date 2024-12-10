import math
from typing import Dict, Union, List, Tuple
from .utils import format_capacitance, format_frequency

class DecapCalculator:
    def __init__(self):
        self.FR4_ER = 4.2  # FR4 dielectric constant
        self.TEMP_COEFFICIENTS = {
            'X7R': (-0.15, 0.15),   # ±15% over temp range
            'X5R': (-0.15, 0.15),   # ±15% over temp range
            'C0G': (-0.03, 0.03),   # ±0.3% over temp range
            'Y5V': (-0.82, 0.22)    # -82% to +22% over temp range
        }

    def calculate_power_decoupling(self, voltage: float, current_draw: float, 
                                 voltage_ripple_percent: float = 5, 
                                 switching_freq: float = None,
                                 temp_range: Tuple[float, float] = (25, 85)) -> Dict[str, float]:
        """Calculate power line decoupling capacitor requirements with temperature considerations"""
        # Base calculations
        voltage_ripple = (voltage_ripple_percent/100) * voltage
        min_capacitance = (current_draw) / (voltage_ripple * switching_freq) if switching_freq else \
                         (current_draw) / (voltage_ripple * 120)
        
        design_capacitance = min_capacitance * 1.5
        max_esr = voltage_ripple / current_draw
        voltage_rating = voltage * 1.5
        
        # Split into multiple capacitors if total capacitance is too large
        MAX_CAP_SIZE = 1000e-6  # Maximum practical capacitor size (1000µF)
        if design_capacitance > MAX_CAP_SIZE:
            num_caps = math.ceil(design_capacitance / MAX_CAP_SIZE)
            cap_per_device = design_capacitance / num_caps
        else:
            num_caps = 1
            cap_per_device = design_capacitance
        
        result = {
            "total_capacitance": design_capacitance,
            "voltage_rating": voltage_rating,
            "max_esr": max_esr,
            "num_capacitors": num_caps,
            "capacitance_per_device": cap_per_device
        }
        
        # Add temperature derating
        temp_derated_cap = self.calculate_temperature_derating(
            design_capacitance,
            'X7R',  # Assume X7R for power decoupling
            temp_range
        )
        
        result.update({
            "temp_derated_capacitance": temp_derated_cap,
            "temperature_range": temp_range
        })
        
        return result

    def calculate_impedance_vs_frequency(self, capacitance: float, esr: float, 
                                      freq_range: Tuple[float, float], 
                                      points: int = 100) -> List[Tuple[float, float]]:
        """Calculate impedance vs frequency curve for a capacitor"""
        freq_points = []
        impedance_points = []
        
        # Calculate frequency points logarithmically
        freq_start = math.log10(freq_range[0])
        freq_end = math.log10(freq_range[1])
        freq_step = (freq_end - freq_start) / (points - 1)
        
        for i in range(points):
            freq = 10 ** (freq_start + i * freq_step)
            
            # Calculate impedance components
            xc = 1 / (2 * math.pi * freq * capacitance)  # Capacitive reactance
            z = math.sqrt(esr**2 + xc**2)  # Total impedance
            
            freq_points.append(freq)
            impedance_points.append(z)
            
        return list(zip(freq_points, impedance_points))

    def calculate_temperature_derating(self, capacitance: float, 
                                    dielectric_type: str,
                                    temp_range: Tuple[float, float]) -> float:
        """Calculate temperature-derated capacitance"""
        if dielectric_type not in self.TEMP_COEFFICIENTS:
            raise ValueError(f"Unknown dielectric type: {dielectric_type}")
            
        min_coef, max_coef = self.TEMP_COEFFICIENTS[dielectric_type]
        temp_min, temp_max = temp_range
        
        # Calculate worst-case capacitance change
        temp_delta = temp_max - 25  # Reference to room temperature
        if temp_delta > 0:
            worst_case_coef = min_coef  # Usually capacitance decreases with temperature
        else:
            worst_case_coef = max_coef
            
        derated_capacitance = capacitance * (1 + worst_case_coef)
        return derated_capacitance 

    def calculate_signal_decoupling(self, signal_freq: float, impedance: float = 50, 
                                  bypass_factor: float = 0.1) -> Dict[str, Union[float, str]]:
        """Calculate signal line decoupling/bypass capacitor requirements"""
        min_capacitance = 1 / (2 * math.pi * signal_freq * impedance * bypass_factor)
        design_capacitance = min_capacitance * 2  # Add 100% margin for safety
        min_srf = signal_freq * 3  # SRF should be at least 3x signal frequency
        
        # Determine recommended capacitor type based on frequency
        if signal_freq < 1e6:
            cap_type = "Ceramic X7R/X5R"
        elif signal_freq < 100e6:
            cap_type = "Ceramic C0G/NP0"
        else:
            cap_type = "RF Ceramic"
        
        # Calculate maximum placement distance
        placement_distance = self.calculate_lambda10_distance(signal_freq)
        
        return {
            "capacitance": design_capacitance,
            "min_srf": min_srf,
            "recommended_type": cap_type,
            "placement_max_distance": placement_distance
        }

    def calculate_lambda10_distance(self, frequency: float) -> float:
        """Calculate maximum decoupling capacitor distance using λ/10 rule"""
        speed_in_fr4 = 299792458 / math.sqrt(self.FR4_ER)  # Speed of light in FR4
        wavelength = speed_in_fr4 / frequency
        return (wavelength / 10) * 1000  # Convert to mm