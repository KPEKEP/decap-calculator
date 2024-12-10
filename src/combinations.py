from typing import List, Tuple, Dict
import math

class CapacitorCombinations:
    @staticmethod
    def parallel_combination(capacitors: List[float]) -> float:
        """Calculate total capacitance for parallel combination"""
        return sum(capacitors)
    
    @staticmethod
    def series_combination(capacitors: List[float]) -> float:
        """Calculate total capacitance for series combination"""
        if not capacitors:
            return 0
        return 1 / sum(1/c for c in capacitors)
    
    @staticmethod
    def find_parallel_combination(target: float, available_values: List[float], 
                                max_components: int = 3) -> List[List[float]]:
        """Find possible parallel combinations to achieve target capacitance"""
        results = []
        available_values = sorted(available_values)
        
        def find_combinations(remaining: float, current: List[float], start_idx: int):
            if len(current) > max_components:
                return
            
            if abs(remaining) < target * 0.01:  # 1% tolerance
                results.append(current.copy())
                return
                
            for i in range(start_idx, len(available_values)):
                if available_values[i] <= remaining:
                    current.append(available_values[i])
                    find_combinations(remaining - available_values[i], current, i)
                    current.pop()
        
        find_combinations(target, [], 0)
        return results
    
    @staticmethod
    def find_series_combination(target: float, available_values: List[float], 
                              max_components: int = 3) -> List[List[float]]:
        """Find possible series combinations to achieve target capacitance"""
        results = []
        available_values = sorted(available_values, reverse=True)
        
        def find_combinations(current: List[float], start_idx: int):
            current_cap = CapacitorCombinations.series_combination(current) if current else float('inf')
            
            if len(current) > max_components:
                return
                
            if abs(current_cap - target) < target * 0.01:  # 1% tolerance
                results.append(current.copy())
                return
                
            for i in range(start_idx, len(available_values)):
                current.append(available_values[i])
                find_combinations(current, i)
                current.pop()
        
        find_combinations([], 0)
        return results 