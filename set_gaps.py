import subprocess
import os
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from utils import get_active_monitor, get_active_workspace, read_config

CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".config", "sway",
                           "scripts", "sway_gaps_manager", "gaps_config.json")

GAPS_OPTIONS = {"inner", "outer", "horizontal", "vertical"}


class ConfigUpdateHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == CONFIG_FILE:
            config = read_config(CONFIG_FILE)

            # because of race conditions this absolutely necessary
            # additional fixes can be made in util.read_config
            # proper file lock would solve these issues

            if config is not None:
                set_gaps(config)

def start_config_watcher():
    event_handler = ConfigUpdateHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(CONFIG_FILE), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(0.1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()


def load_defaults(config):
    """
    load default gaps behavior before monitor specific configuration
    """
    pass


def initial_load(config):
    """Loads initial config file before actively watching the config file"""
    active_ws = get_active_workspace()

    for _, value in config["outputs"].items():
        active_profile_name = value["workspace_profile"]
        assigned_workspaces = value["assigned_workspaces"]
        active_mode = value["active_mode"]
        profile_configuration = config["profiles"][active_profile_name]["modes"][active_mode]

        try:
            for ws in assigned_workspaces:

                # Focus on assigned workspace
                subprocess.run(
                    ["swaymsg", f"workspace {ws}"],
                    capture_output=False,
                    check=True
                )

                # apply gaps settings
                for param, value in profile_configuration.items():
                    if param in GAPS_OPTIONS:
                        subprocess.run(
                            ["swaymsg", f"gaps {param} current set {value}"],
                            capture_output=False,
                            check=True
                        )

            # Finally return back to original workspace
            subprocess.run(
                ["swaymsg", f"workspace {active_ws}"]
            )
        except subprocess.CalledProcessError as e:
            print("Command failed:", e)


def set_gaps(config):

    active_monitor = get_active_monitor()
    monitor_profile = config["outputs"][active_monitor]["workspace_profile"]
    active_mode = config["outputs"][active_monitor]["active_mode"]

    current_settings = config["profiles"][monitor_profile]["modes"][active_mode]

    try:
        for param, value in current_settings.items():

            if param in GAPS_OPTIONS:
                subprocess.run(
                    ["swaymsg", f"gaps {param} current set {value}"],
                    capture_output=False,
                    check=True
                )

    except subprocess.CalledProcessError as e:
        print("Command failed to run:", e)


if __name__ == "__main__":
    
    # Sleep before executing anything to give sway time to load workspaces
    time.sleep(2.5)

    config = read_config(CONFIG_FILE)
    initial_load(config=config)
    start_config_watcher()
