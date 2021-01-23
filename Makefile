test:
	python3 -m unittest discover -s test/ -p "layout_*_test.py"
lint:
	python3 -m pip install flake8 && flake8 .
