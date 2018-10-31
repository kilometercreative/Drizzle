#!/usr/bin/env bash

python setup.py sdist bdist_wheel
pip install ./dist/* --force-reinstall
rm -rf dist