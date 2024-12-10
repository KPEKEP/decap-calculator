from src.calculator import DecapCalculator
from src.combinations import CapacitorCombinations
from src.utils import format_capacitance, format_frequency, format_impedance
import sys

def main():
    calculator = DecapCalculator()
    combinations = CapacitorCombinations()
    
    while True:
        print("\nDecoupling Capacitor Calculator")
        print("==============================")
        print("1. Calculate Power Supply Decoupling")
        print("2. Calculate Signal Line Decoupling")
        print("3. Calculate Lambda/10 Distance")
        print("4. Calculate Impedance vs Frequency")
        print("5. Calculate Capacitor Combinations")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':
            try:
                voltage = float(input("Enter supply voltage (V): "))
                current = float(input("Enter maximum current draw (A): "))
                ripple = float(input("Enter acceptable voltage ripple (%): "))
                freq_str = input("Enter switching frequency (Hz) [press Enter for AC supply]: ")
                
                freq = float(freq_str) if freq_str.strip() else None
                
                result = calculator.calculate_power_decoupling(voltage, current, ripple, freq)
                
                print("\nPower Decoupling Results:")
                print(f"Total Capacitance: {format_capacitance(result['total_capacitance'])}")
                print(f"Voltage Rating: {result['voltage_rating']:.1f}V")
                print(f"Maximum ESR: {result['max_esr']:.3f}Ω")
                print(f"Number of Capacitors: {result['num_capacitors']}")
                print(f"Capacitance per Device: {format_capacitance(result['capacitance_per_device'])}")
                print(f"Temperature Derated Capacitance: {format_capacitance(result['temp_derated_capacitance'])}")
                
            except ValueError as e:
                print("Error: Please enter valid numerical values")
                
        elif choice == '2':
            try:
                freq = float(input("Enter signal frequency (Hz): "))
                impedance = float(input("Enter line impedance (Ω) [default=50]: ") or "50")
                bypass = float(input("Enter desired bypass factor [default=0.1]: ") or "0.1")
                
                result = calculator.calculate_signal_decoupling(freq, impedance, bypass)
                
                print("\nSignal Decoupling Results:")
                print(f"Required Capacitance: {format_capacitance(result['capacitance'])}")
                print(f"Minimum Self-Resonant Frequency: {format_frequency(result['min_srf'])}")
                print(f"Recommended Capacitor Type: {result['recommended_type']}")
                print(f"Maximum Placement Distance: {result['placement_max_distance']:.1f} mm")
                
            except ValueError as e:
                print("Error: Please enter valid numerical values")
                
        elif choice == '3':
            try:
                freq = float(input("Enter frequency (Hz): "))
                distance = calculator.calculate_lambda10_distance(freq)
                
                print(f"\nλ/10 Results:")
                print(f"Frequency: {format_frequency(freq)}")
                print(f"Maximum Distance: {distance:.1f} mm")
                
            except ValueError as e:
                print("Error: Please enter a valid frequency")
                
        elif choice == '4':
            try:
                cap = float(input("Enter capacitance (F): "))
                esr = float(input("Enter ESR (Ω): "))
                freq_start = float(input("Enter start frequency (Hz): "))
                freq_end = float(input("Enter end frequency (Hz): "))
                
                curve = calculator.calculate_impedance_vs_frequency(
                    cap, esr, (freq_start, freq_end))
                
                print("\nImpedance vs Frequency:")
                for freq, z in curve[::10]:  # Print every 10th point
                    print(f"f={format_frequency(freq)}, Z={format_impedance(z)}")
                    
            except ValueError as e:
                print("Error: Please enter valid numerical values")
                
        elif choice == '5':
            try:
                target = float(input("Enter target capacitance (F): "))
                values_str = input("Enter available capacitance values (comma-separated, in F): ")
                available_values = [float(x.strip()) for x in values_str.split(',')]
                
                print("\nParallel Combinations:")
                parallel_results = combinations.find_parallel_combination(
                    target, available_values)
                for combo in parallel_results:
                    print(f"Use: {[format_capacitance(c) for c in combo]}")
                    
                print("\nSeries Combinations:")
                series_results = combinations.find_series_combination(
                    target, available_values)
                for combo in series_results:
                    print(f"Use: {[format_capacitance(c) for c in combo]}")
                    
            except ValueError as e:
                print("Error: Please enter valid numerical values")
                
        elif choice == '6':
            print("Thank you for using the Decoupling Capacitor Calculator!")
            break
            
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()