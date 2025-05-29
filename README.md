# Sway gaps manager 


### What is it?

Simple and barely working gaps manager for sway.
I was annoyed that there was no proper way to manage gaps based on your active monitor
so I made this simple tool to help with it. 

I hope this helps you at least on journey on how to get started

### How to install

```shell
# If this path doesn't already exist
mkdir -p ~/.config/sway/scripts/

cd ~/.config/sway/scripts/
git clone https://gitlab.com/syomasa/sway_gaps_manager.git
```

To your sway config 
```
# ~/.config/sway/config

# This can be any binding I use $mod+f on my config
bindsym $mod + f exec $HOME/.config/sway/scripts/sway_gaps_manager/cycle_modes.sh

exec $HOME/.config/sway/scripts/sway_gaps_manager/start_config_watcher.sh
```

Additionally you need to change from output names from `gaps_config.json` 
to match monitors you want to use.

### How to use

To create new modes/alter existing ones you can edit the `gaps_config.json`file.

```json
{
    "default": {
        "inner": 10,
        "outer": 10
    },

    "outputs": {
        "DP-1": {"active_mode": 0, "workspace_profile": "widescreen", "assigned_workspaces": [1,2]},
        "DP-3": {"active_mode": 0, "workspace_profile": "vertical monitor", "assigned_workspaces": [3]},
        "HDMI-A-1": {"active_mode": 0, "workspace_profile": "tv", "assigned_workspaces": [4]}
    },

    "profiles": {
        "widescreen": {"modes": [
            {"name": "widescreen-centered", "horizontal": 550, "inner": 10},
            {"name": "widescreen-small-gaps", "inner": 10, "outter": 10}
        ]},

        "vertical monitor": {"modes": [{"name": "widescreen-small-gaps", "inner": 10, "outter": 5}]},
        "tv": {"modes":[{"name": "widescreen-small-gaps", "inner": 10, "outter": 10}]}
    }

}
```

You probably only want to edit/add to `profile` or add new devices to `output` sections. 
Editing can be done in similar way as template shows. 

Currently project supports 4 of the gaps options
(inner, outer, vertical, horizontal) there is no plan to add others while it would be quite 
simple just by adding options `GAPS_OPTIONS` variable in `set_gaps.py`
 