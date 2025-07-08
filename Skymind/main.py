from threading import Thread
from telemetry.logger import start_logger
from agents.px4_agent import run_px4_agent
from network.bridge import start_server
from gui.app import launch_gui

if __name__ == "__main__":
    Thread(target=start_logger, daemon=True).start()
    Thread(target=run_px4_agent, daemon=True).start()
    Thread(target=start_server, daemon=True).start()
    launch_gui()
