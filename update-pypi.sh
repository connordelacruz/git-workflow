#!/usr/bin/env bash
set -o errexit
# Build packages
python -m build
# TODO Upload to PyPI
# twine upload dist/*
# Cleanup
rm dist/*

