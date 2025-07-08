from core.state import telemetry
print("[Plugin] Smart Object Tracker Ready")

if "AI" in telemetry["params"] and telemetry["params"]["AI"] == 1:
    print("[Plugin] AI planning engaged.")
