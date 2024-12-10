import unittest
from src.combinations import CapacitorCombinations

class TestCapacitorCombinations(unittest.TestCase):
    def setUp(self):
        self.combinations = CapacitorCombinations()

    def test_parallel_combination_basic(self):
        """Test basic parallel combination"""
        caps = [10e-6, 22e-6, 47e-6]  # 10µF, 22µF, 47µF
        total = self.combinations.parallel_combination(caps)
        self.assertAlmostEqual(total, 79e-6)  # Should be 79µF
        
    def test_parallel_combination_edge_cases(self):
        """Test parallel combination edge cases"""
        # Empty list
        self.assertEqual(self.combinations.parallel_combination([]), 0)
        
        # Single capacitor
        self.assertEqual(self.combinations.parallel_combination([10e-6]), 10e-6)
        
        # Very small values
        small_caps = [1e-12, 2e-12, 3e-12]
        self.assertAlmostEqual(self.combinations.parallel_combination(small_caps), 6e-12)
        
        # Very large values
        large_caps = [1e-3, 2e-3, 3e-3]
        self.assertAlmostEqual(self.combinations.parallel_combination(large_caps), 6e-3)
        
    def test_series_combination_basic(self):
        """Test basic series combination"""
        caps = [10e-6, 10e-6]  # Two 10µF caps in series
        total = self.combinations.series_combination(caps)
        self.assertAlmostEqual(total, 5e-6)  # Should be 5µF
        
    def test_series_combination_edge_cases(self):
        """Test series combination edge cases"""
        # Empty list
        self.assertEqual(self.combinations.series_combination([]), 0)
        
        # Single capacitor
        self.assertEqual(self.combinations.series_combination([10e-6]), 10e-6)
        
        # Different values
        caps = [10e-6, 20e-6, 30e-6]
        expected = 1 / (1/10e-6 + 1/20e-6 + 1/30e-6)
        self.assertAlmostEqual(self.combinations.series_combination(caps), expected)
        
    def test_find_parallel_combination_basic(self):
        """Test finding parallel combinations"""
        available = [10e-6, 22e-6, 47e-6]
        target = 79e-6
        combinations = self.combinations.find_parallel_combination(target, available)
        
        # Check that at least one combination meets the target
        self.assertTrue(any(abs(sum(combo) - target) < target * 0.01 
                          for combo in combinations))
                          
    def test_find_parallel_combination_edge_cases(self):
        """Test finding parallel combinations edge cases"""
        # No solution possible
        combinations = self.combinations.find_parallel_combination(
            100e-6, [1e-6, 2e-6], max_components=2
        )
        self.assertEqual(len(combinations), 0)
        
        # Exact match with single component
        combinations = self.combinations.find_parallel_combination(
            10e-6, [10e-6, 20e-6], max_components=1
        )
        self.assertEqual(len(combinations), 1)
        self.assertEqual(combinations[0], [10e-6])
        
    def test_find_series_combination_basic(self):
        """Test finding series combinations"""
        available = [10e-6, 10e-6, 20e-6]
        target = 5e-6
        combinations = self.combinations.find_series_combination(target, available)
        
        # Check that at least one combination meets the target
        self.assertTrue(any(abs(self.combinations.series_combination(combo) - target) < target * 0.01 
                          for combo in combinations))
                          
    def test_find_series_combination_edge_cases(self):
        """Test finding series combinations edge cases"""
        # No solution possible
        combinations = self.combinations.find_series_combination(
            0.1e-6, [10e-6, 20e-6], max_components=2
        )
        self.assertEqual(len(combinations), 0)
        
        # Target larger than any available capacitor
        combinations = self.combinations.find_series_combination(
            100e-6, [10e-6, 20e-6], max_components=2
        )
        self.assertEqual(len(combinations), 0)