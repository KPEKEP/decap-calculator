import unittest
from src.calculator import DecapCalculator

class TestDecapCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = DecapCalculator()

    def test_power_decoupling_basic(self):
        """Test basic power decoupling calculation"""
        result = self.calculator.calculate_power_decoupling(
            voltage=5.0,
            current_draw=1.0,
            voltage_ripple_percent=5,
            switching_freq=100000
        )
        
        self.assertGreater(result['total_capacitance'], 0)
        self.assertGreater(result['voltage_rating'], 5.0)
        self.assertGreater(result['max_esr'], 0)
        self.assertEqual(result['num_capacitors'], 1)  # Should be 1 for small capacitance
        
    def test_power_decoupling_large_capacitance(self):
        """Test power decoupling with large current that requires multiple capacitors"""
        result = self.calculator.calculate_power_decoupling(
            voltage=12.0,
            current_draw=10.0,
            voltage_ripple_percent=1,  # Tight ripple requirement
            switching_freq=100000
        )
        
        self.assertGreater(result['num_capacitors'], 1)
        self.assertLess(result['capacitance_per_device'], 1000e-6)  # Each cap should be ≤1000µF
        
    def test_power_decoupling_ac_supply(self):
        """Test power decoupling for AC supply (no switching frequency)"""
        result = self.calculator.calculate_power_decoupling(
            voltage=230.0,
            current_draw=0.5,
            voltage_ripple_percent=5,
            switching_freq=None  # AC supply
        )
        
        self.assertGreater(result['total_capacitance'], 0)
        self.assertGreater(result['voltage_rating'], 230.0)
        
    def test_temperature_derating_various_dielectrics(self):
        """Test temperature derating for different dielectric types"""
        test_cap = 100e-6  # 100 µF
        test_cases = [
            ('X7R', (25, 85)),
            ('X5R', (-55, 85)),
            ('C0G', (25, 125)),
            ('Y5V', (0, 85))
        ]
        
        for dielectric, temp_range in test_cases:
            with self.subTest(dielectric=dielectric):
                derated_cap = self.calculator.calculate_temperature_derating(
                    test_cap, dielectric, temp_range
                )
                self.assertGreater(derated_cap, 0)
                
    def test_temperature_derating_invalid_dielectric(self):
        """Test temperature derating with invalid dielectric type"""
        with self.assertRaises(ValueError):
            self.calculator.calculate_temperature_derating(
                100e-6, 'INVALID', (25, 85)
            )
            
    def test_impedance_calculation_frequency_range(self):
        """Test impedance calculations across frequency ranges"""
        test_cases = [
            (100e-6, 0.1, (100, 1e6)),      # Standard case
            (1e-6, 0.01, (1e6, 1e9)),       # High frequency case
            (1000e-6, 1.0, (10, 1000))      # Low frequency case
        ]
        
        for cap, esr, freq_range in test_cases:
            with self.subTest(capacitance=cap, freq_range=freq_range):
                curve = self.calculator.calculate_impedance_vs_frequency(
                    cap, esr, freq_range
                )
                
                self.assertEqual(len(curve), 100)  # Default points
                
                # Check frequency range
                self.assertAlmostEqual(curve[0][0], freq_range[0], delta=freq_range[0]*0.01)
                self.assertAlmostEqual(curve[-1][0], freq_range[1], delta=freq_range[1]*0.01)
                
                # Check impedance values
                for freq, z in curve:
                    self.assertGreater(z, 0)  # Impedance should always be positive
                    self.assertGreater(freq, 0)  # Frequency should always be positive
                    
    def test_edge_cases(self):
        """Test various edge cases"""
        # Test with very small values
        result_small = self.calculator.calculate_power_decoupling(
            voltage=0.1,
            current_draw=0.001,
            voltage_ripple_percent=1
        )
        self.assertGreater(result_small['total_capacitance'], 0)
        
        # Test with very large values
        result_large = self.calculator.calculate_power_decoupling(
            voltage=1000,
            current_draw=100,
            voltage_ripple_percent=0.1
        )
        self.assertGreater(result_large['num_capacitors'], 1)
        
        # Test temperature derating at extreme temperatures
        derated_cap = self.calculator.calculate_temperature_derating(
            100e-6, 'X7R', (-55, 125)
        )
        self.assertGreater(derated_cap, 0)