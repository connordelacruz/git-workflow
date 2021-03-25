#!/usr/bin/env bash
set -o errexit
# Build packages
python -m build
twine upload dist/*
# Cleanup
rm dist/*

