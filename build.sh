#!/bin/bash
set -e
rm dist/*
python3 setup.py sdist
venv/bin/twine upload -r oboro dist/*
