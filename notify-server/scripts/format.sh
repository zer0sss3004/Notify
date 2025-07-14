#!/bin/sh

set -x


autoflake --remove-all-unused-imports --recursive --remove-unused-variables -v --in-place src --exclude=__init__.py
isort src --profile black
black -v --color src
autoflake --remove-all-unused-imports --recursive --remove-unused-variables -v --in-place tests --exclude=__init__.py
isort tests --profile black
black -v --color tests