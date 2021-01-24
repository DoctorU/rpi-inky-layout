.PHONY: python-dist
library/lint:
	cd library; flake8 .
library/test: library/lint
	cd library; python3 -m unittest discover -s test/ -p "layout_*_test.py"
library/build: library/test
library/README.md: README.md
	cp README.md library/
library/LICENSE.txt: LICENSE
	cp LICENSE library/LICENSE.txt

python-readme: library/README.md
python-licence: library/LICENSE.txt
python-clean:
	-rm -r library/dist
	-rm -r library/README.md
	-rm -r library/LICENSE.txt
	-rm -r library/*.egg-info/
python-dist: library/build python-readme python-licence
	cd library; python3 setup.py sdist bdist_wheel

# To get this to work, you had to set up ~/.pypirc with username __token__ and
# your API token.
python-testdeploy: python-dist
	python3 -m twine upload --repository testpypi library/dist/*

# To get this to work, you had to set up ~/.pypirc with username __token__ and
# your API token.
python-deploy: python-dist
	python3 -m twine upload library/dist/*
