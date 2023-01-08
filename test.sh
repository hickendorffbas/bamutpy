#!/usr/bin/env bash

#This runs the tests for bamutpy, its not needed for running the mutation tester itself
#It needs to be run from the main bamutpy directory for the paths to work out!

# we add tests to the python path, so the "testproject" can be correctly discovered by the import module
SCRIPT_DIR=$(pwd)
export PYTHONPATH=$PYTHONPATH:$SCRIPT_DIR/tests

# we run the tests in the testfolder, except the tests in the testproject, because those are the tests that are out input (since bamutpy is processing tests)
pytest -s --ignore=tests/testproject

