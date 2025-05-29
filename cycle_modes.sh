#!/bin/bash
WORK_DIR="$HOME/.config/sway/scripts/sway_gaps_manager"

source $WORK_DIR/venv/bin/activate
python $WORK_DIR/manage_gaps.py
