#/#!/usr/bin/env sh
test -f './version.old'
test -f './version'
old_version="`cat ./version.old`"
version="`cat ./version`"
test "${old_version}" != "${version}" | { echo "ERROR: Versions match!" && exit 1; }
