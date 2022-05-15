check-all:
	python -m black --check pdf_renderer config.py
	python -m pylint pdf_renderer config.py
	python -m flake8 pdf_renderer config.py
	@echo "\033[0;32m === Check is OK === \033[0m"

fix:
	python -m black pdf_renderer config.py
