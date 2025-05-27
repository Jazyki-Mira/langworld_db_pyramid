#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd ${SCRIPT_DIR}/../

echo "Applying alembic migrations (if any)"
pipenv run alembic -c config/production.ini upgrade head

echo "Re-populating the database"
pipenv run initialize_langworld_db_pyramid_db config/production.ini

echo "Compiling translated strings for internationalization"
pipenv run pybabel compile --directory=langworld_db_pyramid/locale --locale=en
