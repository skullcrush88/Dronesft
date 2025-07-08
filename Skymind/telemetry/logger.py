import csv, time
from core.state import telemetry

def start_logger():
    with open("telemetry_log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time", "altitude", "battery", "mode", "failsafe", "gps"])
        while True:
            row = [time.time(), telemetry["altitude"], telemetry["battery"],
                   telemetry["mode"], telemetry["failsafe"], telemetry["gps"]]
            writer.writerow(row)
            f.flush()
            time.sleep(2)
