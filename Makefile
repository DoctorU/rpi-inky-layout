BUILDVER_FILE=.release/build
IMG_EG_SRC=library/test/expected-images
IMG_EG_DOC=doc/img/examples
include .release/release_config

.PHONY: python-newbuild
library/lint:
	cd library; flake8 . --statistics
library/test: library/lint
	mkdir -p library/test/expected-images/
	cd library; python3 -m unittest -b -v
library/build: library/test
library/README.md: README.md
	cp README.md library/
library/LICENSE.txt: LICENSE
	cp LICENSE library/LICENSE.txt
library: library/build library/README.md library/LICENSE.txt

git-pull:
	git pull --all --prune

release-docs:
	test -d '$(IMG_EG_SRC)'
	mkdir -p '$(IMG_EG_DOC)'
	rm $(IMG_EG_DOC)/*.png

	cp $(IMG_EG_SRC)/test-alternatePackingMode.png $(IMG_EG_DOC)/alternatePackingMode.png
	cp $(IMG_EG_SRC)/test-packingBias.png $(IMG_EG_DOC)/packingBias.png
	cp $(IMG_EG_SRC)/test-rotated-UP-add-3-layers.png $(IMG_EG_DOC)/rotation_UP.png
	cp $(IMG_EG_SRC)/test-rotated-LEFT-add-3-layers.png $(IMG_EG_DOC)/rotation_LEFT.png
	cp $(IMG_EG_SRC)/test-rotated-DOWN-add-3-layers.png $(IMG_EG_DOC)/rotation_DOWN.png
	cp $(IMG_EG_SRC)/test-rotated-RIGHT-add-3-layers.png $(IMG_EG_DOC)/rotation_RIGHT.png

release-precheck:
	echo "VERSION: ${VERSION}"
	echo "RELEASE_FROM: ${RELEASE_FROM}"
	test -n "${VERSION}" || { echo "VERSION invalid" && exit 1; }

release-reset: release-precheck
	git restore 'library/setup.py' '.release/build'
	git tag -d 'v${VERSION}' && git push --delete origin 'v${VERSION}'

release-branch:
	git stash
	git fetch --all --tags
	git checkout main

release-newbuild:
	cd .release; ./increment-build.sh
	git add '.release/build'

release-update-setup: release-precheck release-newbuild
	echo "VERSION:${VERSION}"
	sed -e "s:\%GITVER\%:${VERSION}:" 'library/setup.py.template' > 'library/setup.py'
	git add 'library/setup.py'

release: library/test release-precheck release-branch release-update-setup
	git restore "library/test"
	git commit -m"Release ${VERSION}"
	# git tag will fail if the tag already exists.
	git tag "v${VERSION}" -a -m"Release v${VERSION} (`date +'%Y-%m-%d'`)"
	git push origin "v${VERSION}"
	git push origin main

python-clean:
	-rm -r library/dist
	-rm -r library/README.md
	-rm -r library/LICENSE.txt
	-rm -r library/*.egg-info/
python-dist: library
	cd library; python3 setup.py sdist bdist_wheel
# To get this to work, you had to set up ~/.pypirc with username __token__ and
# your API token.
python-testdeploy: python-dist
	python3 -m twine upload --repository testpypi library/dist/*
# To get this to work, you had to set up ~/.pypirc with username __token__ and
# your API token.
python-deploy: python-dist
	python3 -m twine upload library/dist/*
