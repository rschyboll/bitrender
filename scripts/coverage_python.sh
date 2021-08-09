#!/bin/bash
source /home/hoodrobinrs/Documents/Rendering_Server/.venv/bin/activate
python -m coverage run --source ./ --rcfile=../.coveragerc  -m pytest &> /dev/null
python -m coverage report
python -m coverage erase