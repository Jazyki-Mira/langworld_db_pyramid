#!/bin/bash

# pulls project from repository, re-populates the database, re-compiles localization message catalog

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd ${SCRIPT_DIR}/../

git fetch origin
git merge origin/master

pipenv install

${SCRIPT_DIR}/init_compile.sh
