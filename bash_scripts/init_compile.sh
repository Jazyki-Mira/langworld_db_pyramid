#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd ${SCRIPT_DIR}/../

echo "Applying alembic migrations (if any)"
alembic -c config/production.ini upgrade head

echo "Re-populating the database"
initialize_langworld_db_pyramid_db config/production.ini

echo "Compiling translated strings for internationalization"
pybabel compile --directory=langworld_db_pyramid/locale --locale=en
