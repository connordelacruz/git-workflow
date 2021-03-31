#!/usr/bin/env bash
set -o errexit
# Build packages
python -m build
# TODO args for testpypi
# twine upload --repository testpypi dist/*
twine upload dist/*
# Cleanup
rm dist/*

