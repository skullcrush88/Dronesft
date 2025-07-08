import os

def load_plugins():
    print("[SkyMind] Loading plugins...")
    for file in os.listdir("plugins"):
        if file.endswith(".py"):
            try:
                exec(open(f"plugins/{file}").read(), globals())
                print(f"[SkyMind] Loaded plugin: {file}")
            except Exception as e:
                print(f"[SkyMind] Plugin error ({file}):", e)
