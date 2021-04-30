#!/usr/bin/env bash
set -o errexit
arg_test=
while getopts 't' opt; do
    case ${opt} in
        t)
            arg_test=1
            ;;
    esac
done
shift $((OPTIND -1))
# Build packages
python -m build
# Upload
if [[ -z "$arg_test" ]]; then
    twine upload dist/*
else
    twine upload --repository testpypi dist/*
fi
# Cleanup
rm dist/*

