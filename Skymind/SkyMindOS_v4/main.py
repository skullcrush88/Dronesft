from threading import Thread
from core.state import telemetry
from core.plugins import load_plugins
from agents.px4_agent import run_px4_agent
from network.bridge import start_server
from telemetry.logger import start_logger
from gui.app import launch_gui

if __name__ == "__main__":
    Thread(target=start_logger, daemon=True).start()
    Thread(target=run_px4_agent, daemon=True).start()
    Thread(target=start_server, daemon=True).start()
    load_plugins()
    launch_gui()
