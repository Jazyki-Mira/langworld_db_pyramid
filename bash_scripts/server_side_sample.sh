#!/bin/bash

# pulls project from repository, re-populates the database, re-compiles localization message catalog

# strict mode: make sure errors don't pass silently
set -euo pipefail

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd ${SCRIPT_DIR}/../

git fetch origin
git reset --hard origin/master

pip install pipenv
pipenv install

${SCRIPT_DIR}/init_compile.sh

# For PythonAnywhere: touching WSGI file is equivalent to clicking "Reload Web App" button
# https://help.pythonanywhere.com/pages/ReloadWebApp/
# Replace with actual path to WSGI file
touch /var/www/<file_name_wsgi>.py
