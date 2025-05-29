import json
import os
import sys

from utils import get_active_monitor, read_config

CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".config", "sway",
                           "scripts", "sway_gaps_manager", "gaps_config.json")

def cycle_modes(config):

    active_monitor = get_active_monitor()

    current_profile = config["outputs"][active_monitor]["workspace_profile"]
    ammount_of_modes_for_profile = len(config["profiles"][current_profile]["modes"])

    if ammount_of_modes_for_profile == 1:
        # No need to write in file if there is no modes to cycle through
        return None

    # Step 1 mode forward
    config["outputs"][active_monitor]["active_mode"] += 1
    config["outputs"][active_monitor]["active_mode"] %= ammount_of_modes_for_profile

    # Write back to file. This should trigger the watchdog on set_gaps.py file

    try:
        with open(CONFIG_FILE, "w") as fp:
            json.dump(config, fp, indent=4)

    except FileNotFoundError:
        print(f"Could not find config file {CONFIG_FILE}, exiting")
        sys.exit(1)


if __name__ == "__main__":
    config = read_config(CONFIG_FILE)
    cycle_modes(config)
