#/usr/bin/env bash
# === Docker entrypoint for API application ===
# =============================================
pipenv run flask db upgrade
pipenv run flask run --host 0.0.0.0 --port 5000
