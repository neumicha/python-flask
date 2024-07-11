# Python Flask Example

## Setup
Unix/macOS:
- `python3 -m venv ./.venv`
- `source ./.venv/Scripts/activate`
- `python3 -m pip install --upgrade pip`
- `python3 -m pip install -r requirements.txt`

Windows:
- `py -m venv .\.venv`
- For CMD: `.\.venv\Scripts\activate.bat`
- For PowerShell: `.\.venv\Scripts\Activate.ps1`
- `py -m pip install --upgrade pip`
- `py -m pip install -r requirements.txt`

## Run
Development mode:
- `flask run`
Debug mode:
- `flask run --debug`

## How to
### Freeze dependencies
Unix/macOS:
- `python3 -m pip freeze > requirements.txt`

Windows:
- `py -m pip freeze > requirements.txt`

## Notes
- Tested with Python 3.12.4