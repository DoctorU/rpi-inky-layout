#!/bin/sh
VERSION="${1}"
test -n "${VERSION}" || { echo "ERROR: version  not set: ${VERSION}";exit 1; }
PATCH=`echo "${VERSION}" | awk -F'.' '{print $3}'`
echo "PATCH: ${PATCH}"
test -n "${PATCH}" || { echo "ERROR: invalid version format - not x.x.x: ${VERSION}";exit 1; }
echo "VERSION: ${VERSION} - PATCH: ${PATCH}"
echo "${VERSION}" > 'version'
