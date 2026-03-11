"""
Deloitte Graduate Hiring – Automobile Testing & Engineering Assessment
======================================================================
Candidate  : Manoj B S
Email      : bsmanoj65@gmail.com
College    : Alliance University, Bangalore
Skill Track: Automobile Testing & Engineering

Tasks Covered:
  1. Vehicle Diagnostics System (OBD-II Simulation)
  2. Engine Performance Calculator
  3. Fuel Efficiency & Emissions Analysis
  4. Brake & Safety System Testing
  5. Test Report Generator
"""

import math
import json
import random
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple

random.seed(42)

# ─────────────────────────────────────────────────────────────
# DATA MODELS
# ─────────────────────────────────────────────────────────────

@dataclass
class Vehicle:
    vin:          str
    make:         str
    model:        str
    year:         int
    engine_cc:    int       # displacement in cc
    fuel_type:    str       # petrol / diesel / electric / hybrid
    odometer_km:  float
    max_power_hp: int

    def __str__(self):
        return f"{self.year} {self.make} {self.model} [{self.vin}]"


@dataclass
class OBDFaultCode:
    code:        str
    description: str
    severity:    str   # CRITICAL / WARNING / INFO
    subsystem:   str


@dataclass
class TestResult:
    test_name:   str
    passed:      bool
    value:       float
    unit:        str
    threshold:   float
    notes:       str = ""


# ─────────────────────────────────────────────────────────────
# TASK 1 – OBD-II Diagnostics Simulation
# ─────────────────────────────────────────────────────────────
print("=" * 65)
print("TASK 1: OBD-II Vehicle Diagnostics Simulation")
print("=" * 65)

FAULT_CODE_DB: Dict[str, OBDFaultCode] = {
    "P0300": OBDFaultCode("P0300", "Random/Multiple Cylinder Misfire",       "CRITICAL", "Engine"),
    "P0171": OBDFaultCode("P0171", "System Too Lean (Bank 1)",               "WARNING",  "Fuel System"),
    "P0420": OBDFaultCode("P0420", "Catalyst System Efficiency Below Threshold","WARNING","Exhaust"),
    "P0442": OBDFaultCode("P0442", "Evaporative Emission Small Leak",        "INFO",     "EVAP System"),
    "P0507": OBDFaultCode("P0507", "Idle Control System RPM High",           "WARNING",  "Engine"),
    "C0040": OBDFaultCode("C0040", "Right Front Wheel Speed Sensor Circuit", "CRITICAL", "ABS/Brakes"),
    "B0010": OBDFaultCode("B0010", "Driver Frontal Stage 1 Deployment",      "CRITICAL", "Airbag"),
    "U0100": OBDFaultCode("U0100", "Lost Communication With ECM/PCM",        "CRITICAL", "Network"),
}

def run_obd_scan(vehicle: Vehicle, fault_codes: List[str]) -> Dict:
    print(f"\n  Vehicle : {vehicle}")
    print(f"  Odometer: {vehicle.odometer_km:,.0f} km")
    print(f"  Scanning for fault codes...\n")

    faults      = []
    clear_count = 0

    for code in fault_codes:
        if code in FAULT_CODE_DB:
            fc = FAULT_CODE_DB[code]
            faults.append(fc)
            icon = "🔴" if fc.severity == "CRITICAL" else ("🟡" if fc.severity == "WARNING" else "🔵")
            print(f"  {icon} [{fc.severity:8s}] {fc.code} – {fc.description}")
            print(f"           Subsystem: {fc.subsystem}")
        else:
            clear_count += 1

    if not faults:
        print("  ✅ No fault codes detected – vehicle is healthy.")
    else:
        critical = sum(1 for f in faults if f.severity == "CRITICAL")
        warnings = sum(1 for f in faults if f.severity == "WARNING")
        info     = sum(1 for f in faults if f.severity == "INFO")
        print(f"\n  Summary: {len(faults)} fault(s) found – "
              f"{critical} critical, {warnings} warnings, {info} info")

    return {"vehicle": str(vehicle), "faults": [asdict(f) for f in faults]}


car1 = Vehicle("MH12AB1234", "Tata",   "Nexon",    2022, 1497, "petrol",  32500, 120)
car2 = Vehicle("KA05CD5678", "Maruti", "Brezza",   2021, 1462, "petrol",  48200, 103)
car3 = Vehicle("DL01EF9012", "Mahindra","Scorpio-N",2023, 2184, "diesel",  12000, 175)

run_obd_scan(car1, ["P0171", "P0442"])
run_obd_scan(car2, ["P0300", "C0040", "P0420"])
run_obd_scan(car3, [])


# ─────────────────────────────────────────────────────────────
# TASK 2 – Engine Performance Calculator
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("TASK 2: Engine Performance Calculator")
print("=" * 65)

def calculate_torque(power_kw: float, rpm: float) -> float:
    """Torque (Nm) = (Power_kW × 1000 × 60) / (2π × RPM)"""
    return (power_kw * 1000 * 60) / (2 * math.pi * rpm)

def calculate_bmep(torque_nm: float, displacement_cc: float, cylinders: int) -> float:
    """Brake Mean Effective Pressure (bar) = (4π × Torque) / (Displacement_m³)"""
    displacement_m3 = (displacement_cc / 1e6)
    return (4 * math.pi * torque_nm) / (displacement_m3 * 1e5)   # convert Pa→bar

def hp_to_kw(hp: float) -> float:
    return hp * 0.7457

def power_to_weight_ratio(power_hp: float, weight_kg: float) -> float:
    return round(power_hp / weight_kg, 3)

vehicles_perf = [
    {"name": "Tata Nexon 1.2T",    "hp": 120, "rpm": 5000, "cc": 1497, "cyl": 4, "weight": 1250},
    {"name": "Maruti Brezza 1.5",  "hp": 103, "rpm": 6000, "cc": 1462, "cyl": 4, "weight": 1190},
    {"name": "Mahindra Scorpio 2.2","hp": 175, "rpm": 3750, "cc": 2184, "cyl": 4, "weight": 2050},
    {"name": "Hyundai i20 1.0T",   "hp": 120, "rpm": 6000, "cc":  998, "cyl": 3, "weight": 1100},
]

print(f"\n  {'Vehicle':<26} {'Power(kW)':>9} {'Torque(Nm)':>10} {'BMEP(bar)':>9} {'P/W':>8}")
print("  " + "-" * 70)
for v in vehicles_perf:
    kw    = hp_to_kw(v["hp"])
    torq  = calculate_torque(kw, v["rpm"])
    bmep  = calculate_bmep(torq, v["cc"], v["cyl"])
    pw    = power_to_weight_ratio(v["hp"], v["weight"])
    print(f"  {v['name']:<26} {kw:>9.1f} {torq:>10.1f} {bmep:>9.2f} {pw:>8.3f}")


# ─────────────────────────────────────────────────────────────
# TASK 3 – Fuel Efficiency & Emissions Analysis
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("TASK 3: Fuel Efficiency & CO₂ Emissions Analysis")
print("=" * 65)

CO2_PER_LITRE = {"petrol": 2.31, "diesel": 2.68, "hybrid": 1.40, "electric": 0.0}

@dataclass
class FuelTestRecord:
    vehicle_name: str
    fuel_type:    str
    distance_km:  float
    fuel_used_l:  float

    @property
    def mileage_kmpl(self) -> float:
        return self.distance_km / self.fuel_used_l if self.fuel_used_l > 0 else float("inf")

    @property
    def co2_grams_per_km(self) -> float:
        co2_per_l = CO2_PER_LITRE.get(self.fuel_type, 2.31)
        return (self.fuel_used_l / self.distance_km) * co2_per_l * 1000

fuel_records = [
    FuelTestRecord("Tata Nexon 1.2T",     "petrol",  500, 36.2),
    FuelTestRecord("Maruti Brezza 1.5",   "petrol",  500, 33.5),
    FuelTestRecord("Mahindra Scorpio 2.2","diesel",  500, 31.0),
    FuelTestRecord("Hyundai Creta Hybrid","hybrid",  500, 24.0),
    FuelTestRecord("Tata Nexon EV",       "electric",500,  0.0),   # EV – no fuel
]

# Fix EV display
EURO_6_CO2_LIMIT = 95   # g/km

print(f"\n  {'Vehicle':<26} {'Fuel':>8} {'KMPL':>6} {'CO₂(g/km)':>10} {'Euro 6 ✓'}")
print("  " + "-" * 68)
for r in fuel_records:
    if r.fuel_type == "electric":
        print(f"  {r.vehicle_name:<26} {'EV':>8} {'∞':>6} {'0.0':>10}  ✅ (Zero emission)")
    else:
        co2 = r.co2_grams_per_km
        status = "✅ PASS" if co2 <= EURO_6_CO2_LIMIT else "❌ FAIL"
        print(f"  {r.vehicle_name:<26} {r.fuel_type:>8} {r.mileage_kmpl:>6.1f} {co2:>10.1f}  {status}")


# ─────────────────────────────────────────────────────────────
# TASK 4 – Brake & Safety System Testing
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("TASK 4: Brake & Safety System Testing")
print("=" * 65)

def stopping_distance(speed_kmh: float, decel_g: float = 0.8) -> float:
    """s = v² / (2 × a)  where a = decel_g × 9.81"""
    v_ms = speed_kmh / 3.6
    a    = decel_g * 9.81
    return (v_ms ** 2) / (2 * a)

def reaction_distance(speed_kmh: float, reaction_s: float = 1.5) -> float:
    return (speed_kmh / 3.6) * reaction_s

def total_braking_distance(speed_kmh: float, decel_g: float = 0.8,
                            reaction_s: float = 1.5) -> float:
    return stopping_distance(speed_kmh, decel_g) + reaction_distance(speed_kmh, reaction_s)

ADAS_THRESHOLDS = {
    "ABS Activation Wheel Slip (%)":      (15, 25),
    "ESC Yaw Rate Deviation (°/s)":       ( 0, 10),
    "TPMS Pressure Drop (PSI)":           ( 0,  5),
    "Airbag Deploy Trigger (g-force)":    (10, 20),
    "Lane Keep Assist Latency (ms)":      ( 0,150),
}

print("\n  Braking Distance Analysis:")
print(f"  {'Speed (km/h)':<16} {'Reaction (m)':>14} {'Braking (m)':>12} {'Total (m)':>10}")
print("  " + "-" * 58)
for spd in [40, 60, 80, 100, 120]:
    rd = reaction_distance(spd)
    bd = stopping_distance(spd)
    td = total_braking_distance(spd)
    print(f"  {spd:<16} {rd:>14.1f} {bd:>12.1f} {td:>10.1f}")

print("\n  ADAS / Safety System Test Results:")
results: List[TestResult] = []
for test_name, (lo, hi) in ADAS_THRESHOLDS.items():
    val    = round(random.uniform(lo * 0.7, hi * 1.1), 2)
    passed = lo <= val <= hi
    tr     = TestResult(test_name, passed, val, "", hi, "Within spec" if passed else "OUT OF SPEC")
    results.append(tr)
    icon = "✅" if passed else "❌"
    print(f"  {icon} {test_name:<42} Value: {val:>7.2f}  Limit: {hi}")

passed_count = sum(1 for r in results if r.passed)
print(f"\n  Safety Tests: {passed_count}/{len(results)} PASSED")


# ─────────────────────────────────────────────────────────────
# TASK 5 – Test Report Generator
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("TASK 5: Automated Test Report Generator")
print("=" * 65)

report = {
    "report_id":   "DLT-AUTO-2025-001",
    "generated_at": datetime.now().isoformat(),
    "candidate": {
        "name":       "[Your Full Name]",
        "email":      "[Your Email]",
        "college":    "[Your College Name]",
        "track":      "Automobile Testing & Engineering"
    },
    "vehicles_tested": [str(car1), str(car2), str(car3)],
    "task_summary": {
        "Task 1 – OBD Diagnostics":   "COMPLETED",
        "Task 2 – Engine Performance":"COMPLETED",
        "Task 3 – Fuel & Emissions":  "COMPLETED",
        "Task 4 – Brake & Safety":    "COMPLETED",
        "Task 5 – Report Generation": "COMPLETED",
    },
    "overall_status": "ALL TASKS COMPLETED SUCCESSFULLY",
    "safety_score": f"{passed_count}/{len(results)} safety checks passed",
}

report_path = "test_report.json"
with open(report_path, "w") as f:
    json.dump(report, f, indent=2)
print(f"\n  Report saved → {report_path}")
print(f"  Report ID   : {report['report_id']}")
print(f"  Generated At: {report['generated_at']}")

print("\n" + "=" * 65)
print("  ALL TASKS COMPLETED SUCCESSFULLY")
print("  Candidate: [Your Full Name] | Track: Automobile Testing & Engineering")
print("=" * 65)
