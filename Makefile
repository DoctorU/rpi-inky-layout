BUILDVER_FILE=release/build

.PHONY: python-newbuild
library/lint:
	cd library; flake8 . --statistics
library/test: library/lint
	cd library; python3 -m unittest discover -s test/ -p "layout_*_test.py"
library/build: library/test
library/README.md: README.md
	cp README.md library/
library/LICENSE.txt: LICENSE
	cp LICENSE library/LICENSE.txt

python-readme: library/README.md
python-licence: library/LICENSE.txt
release-precheck: library/test
	test -n "$(VERSION)" || { echo "ERROR: VERSION undefined." && exit 1; }
	echo "Preflight check passed. Proceeding..."
git-pull:
	git pull --all --prune
release-newbuild: git-pull release-precheck
	cd release; ./increment-build.sh
release-branch: release-newbuild
	git checkout -b "release/$(VERSION)"
	cat release/build
	git branch -v
	git tag "v$(VERSION)" -a -m"Release v$(VERSION) (`date +'%Y-%m-%d'`)"
release-reset: release-precheck
	git checkout main
	git tag -d "v$(VERSION)"
	git branch -d "release/$(VERSION)"
	git restore release/build
release: release-branch
	echo "VERSION:$(VERSION)"
	sed -e "s:\%GITVER\%:$(VERSION):" 'library/setup.py.template' > 'library/setup.py'
	echo git add 'library/setup.py' "$(VERSION_FILE)" "$(VERSION_FILE).old"
	echo git commit -m"Release $(VERSION)"
	echo git tag "v$(VERSION)" -a"Release v$(VERSION) (`date +'%Y-%m-%d'`)"

python-clean:
	-rm -r library/dist
	-rm -r library/README.md
	-rm -r library/LICENSE.txt
	-rm -r library/*.egg-info/

python-dist: library/build python-readme python-licence python-version
	cd library; python3 setup.py sdist bdist_wheel

# To get this to work, you had to set up ~/.pypirc with username __token__ and
# your API token.
python-testdeploy: python-dist
	python3 -m twine upload --repository testpypi library/dist/*

# To get this to work, you had to set up ~/.pypirc with username __token__ and
# your API token.
python-deploy: python-dist
	python3 -m twine upload library/dist/*
