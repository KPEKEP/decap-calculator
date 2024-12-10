# Decoupling Capacitor Calculator

A comprehensive tool for calculating decoupling and bypass capacitor requirements in electronic designs.

## Features

- Power Supply Decoupling Calculations
  - Calculates required capacitance based on voltage and current requirements
  - Handles both AC and switching power supplies
  - Includes temperature derating calculations
  - Automatically splits large capacitance values into practical combinations

- Signal Line Decoupling
  - Calculates bypass capacitor requirements for signal integrity
  - Recommends appropriate capacitor types based on frequency
  - Includes λ/10 placement distance calculations
  - Considers impedance and bypass factor requirements

- Impedance vs Frequency Analysis
  - Calculates impedance curves for capacitors
  - Considers ESR effects
  - Logarithmic frequency sweep

- Capacitor Combination Calculator
  - Finds optimal series/parallel combinations
  - Supports multiple capacitor values
  - Helps achieve target capacitance with standard values

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/decap-calculator.git
cd decap-calculator
```

2. Install dependencies (if any):
```bash
pip install -r requirements.txt
```

## Usage

Run the main program:
```bash
python main.py
```

### Example Calculations

1. Power Supply Decoupling:
```python
# For a 5V supply with 1A current draw
voltage = 5.0
current = 1.0
ripple = 5  # 5% ripple
freq = 100000  # 100kHz switching frequency
```

2. Signal Line Decoupling:
```python
# For a 100MHz digital signal
freq = 100e6
impedance = 50  # 50Ω line impedance
bypass_factor = 0.1  # Standard bypass factor
```

## Project Structure

- `src/`
  - `calculator.py`: Core calculation engine
  - `combinations.py`: Capacitor combination algorithms
  - `utils.py`: Utility functions for formatting
- `tests/`
  - Unit tests for all components
- `main.py`: Command-line interface

## Testing

Run the test suite:
```bash
python -m unittest discover tests
```

## Technical Details

### Temperature Derating

Supports multiple dielectric types:
- X7R: ±15% over temperature range
- X5R: ±15% over temperature range
- C0G/NP0: ±0.3% over temperature range
- Y5V: -82% to +22% over temperature range

### Capacitor Selection Guidelines

1. Power Decoupling:
   - Uses 50% design margin
   - Maximum single capacitor size: 1000µF
   - Automatic parallel combination for larger values

2. Signal Decoupling:
   - < 1MHz: X7R/X5R ceramic
   - 1MHz - 100MHz: C0G/NP0 ceramic
   - > 100MHz: RF ceramic
   - λ/10 rule for placement distance

## License

This project is licensed under the MIT License - see the LICENSE file for details.