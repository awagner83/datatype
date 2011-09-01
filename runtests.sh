#!/bin/bash

py.test \
    --ignore=setup.py \
    --cov=datatype \
    --cov-report=term-missing \
    --doctest-glob=README.rst \
    --doctest-modules

