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
	cd library; python3 setup.py sdist

python-testdeploy: python-dist
		twine upload --repository-url https://test.pypi.org/legacy/ library/dist/*

python-deploy: python-dist
		twine upload library/dist/*
