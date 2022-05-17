#/usr/bin/env bash
# === Docker entrypoint for Dramatiq workers ===
# ==============================================
pipenv run dramatiq pdf_renderer.dramatiq_runner:broker --processes 1
