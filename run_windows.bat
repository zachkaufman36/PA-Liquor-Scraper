if not exist "venv" (
    python -m venv venv
)

call venv\scripts\activate
pip install -r requirements.txt
python scraping.py
rd /s /q output

exit