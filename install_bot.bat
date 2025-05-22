@echo off
cmd /k "py -m venv venv & cd /d .\venv\Scripts & activate & cd /d ..\..\ & pip install -r requirements.txt"