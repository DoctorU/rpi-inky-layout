test:
	python3 -m unittest layout_*_test.py
lint:
	python3 -m pip install flake8 && flake8 .
