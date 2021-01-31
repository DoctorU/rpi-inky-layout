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

git-pull:
	git pull --all --prune

release-precheck:
	test -n "$(VERSION)" || { echo "ERROR: VERSION undefined." && exit 1; }
	echo "Preflight check passed. Proceeding..."

release-reset: release-precheck
	git restore 'library/setup.py' 'release/build'
	git tag -d 'v$(VERSION)' && git push --delete origin 'v$(VERSION)'

release-branch:
	git stash
	git fetch --all --tags
	git checkout main

release-newbuild:
	cd release; ./increment-build.sh
	git add 'release/build'

release-update-setup: release-newbuild
	echo 'VERSION:$(VERSION)'
	sed -e "s:\%GITVER\%:$(VERSION):" 'library/setup.py.template' > 'library/setup.py'
	git add 'library/setup.py'

release: library/test release-precheck release-branch release-update-setup
	git restore "library/test"
	git commit -m"Release $(VERSION)"
	git tag "v$(VERSION)" -a -m"Release v$(VERSION) (`date +'%Y-%m-%d'`)"
	git push origin 'v$(VERSION)'

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
