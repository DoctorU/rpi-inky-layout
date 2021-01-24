.PHONY: library/lint

library/clean:
	-rm library/LICENSE.txt library/README.rst; echo "Cleaned."

library/lint:
	cd library; flake8 .
library/test: library/lint
	cd library; python3 -m unittest discover -s test/ -p "layout_*_test.py"


library/README.rst: README.md
	pandoc --from=markdown --to=rst -o library/README.rst README.md
library/LICENSE.txt: LICENSE
	cp LICENSE library/LICENSE.txt

python-readme: library/README.rst
python-licence: library/LICENSE.txt
python-clean:
	-rm -r library/dist
python-dist: library/test python-readme python-licence
	cd library; python3 setup.py sdist

python-testdeploy: python-dist
		twine upload --repository-url https://test.pypi.org/legacy/ library/dist/*

python-deploy: python-dist
		twine upload library/dist/*
