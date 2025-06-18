#!/bin/bash

venv_gui\Scripts\activate

pyinstaller --onefile --windowed --add-data "json_files;json_files" gui.py