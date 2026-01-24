#!/bin/sh
export PYTHONPATH=.
export FHOMM_DATA=~/Downloads/homm/data

ipython3 -i \
         --simple-prompt \
         --InteractiveShellApp.extensions autoreload \
         --InteractiveShellApp.exec_lines '%autoreload 2' \
         -- \
         ./fhomm/main.py \
         --background
