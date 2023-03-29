#!/bin/env bash

set -euo pipefail

if [[ -n ${1:-} ]]; then
  version=${1}
elif [[ -n ${CIRCLE_TAG:-} ]]; then
  version=${CIRCLE_TAG}
else
  version="0.0.0"
fi

echo "${version}" > greas3/VERSION

rm -rf dist
python setup.py bdist_wheel
rm -rf build
