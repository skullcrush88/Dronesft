import json
from core.state import telemetry

def handle_command(raw):
    try:
        data = json.loads(raw)
        cmd = data.get("command", "unknown")
        params = data.get("params", {})
        telemetry["last_command"] = cmd

        if cmd == "takeoff":
            telemetry["altitude"] = float(params.get("altitude", 3))
            print(f"[SkyMind] TAKEOFF to {telemetry['altitude']}m")
        elif cmd == "land":
            telemetry["altitude"] = 0
            print("[SkyMind] LANDING")
        elif cmd == "set_mode":
            telemetry["mode"] = params.get("mode", "GUIDED")
        elif cmd == "disarm":
            telemetry["failsafe"] = True
        elif cmd == "mission":
            for step in params.get("steps", []):
                handle_command(json.dumps(step))
        elif cmd == "analyze":
            print("[SkyMind] Analyzing environment...")
        elif cmd == "trigger":
            if telemetry["battery"] < float(params.get("battery_threshold", 10.8)):
                print("[SkyMind] Trigger met, landing...")
                handle_command(json.dumps({"command": "land"}))
        elif cmd == "param":
            name = params.get("name", "undefined")
            value = params.get("value", None)
            telemetry["params"][name] = value
            print(f"[SkyMind] Set param {name} = {value}")
        elif cmd == "geofence":
            telemetry["geofence"] = params
            print(f"[SkyMind] Geofence set to: {params}")
        else:
            print(f"[SkyMind] Unknown command: {cmd}")
    except Exception as e:
        print(f"[SkyMind] Router ERROR: {e}")
