@echo off
pyinstaller --onefile --noconsole --icon resources\good-head-wink.ico --add-data resources;resources main.py
