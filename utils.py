import json
import sys
import subprocess


def read_config(path: str):
    with open(path, "r") as fp:
        try:
            config = json.load(fp)

        except json.JSONDecodeError:
            print(f"Warning: There was a problem loading {path}",
                  "Check that config is written in proper json.", file=sys.stderr)

            return None

        return config


def get_active_monitor():
    command = "swaymsg -t get_outputs | jq -r '.[] | \
               select(.focused == true).name'"

    process = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        check=True
    )

    output_name = process.stdout.strip()

    if output_name:
        return output_name

    else:
        print("Warning: No focussed display found", file=sys.stderr)
        return None


def get_active_workspace():
    command = "swaymsg -t get_workspaces | jq -r '.[] | \
               select(.focused == true).name'"

    process = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        check=True
    )

    output = process.stdout.strip()

    if output:
        return output
    else:
        print("Warning: No active workspace found", file=sys.stderr)
        return None
