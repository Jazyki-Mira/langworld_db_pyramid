#!/bin/bash

# pulls data from langworld_db_data repository (subtree) and re-populates the SQL database

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd ${SCRIPT_DIR}/../

echo "Downloading data: an editor will be opened for you to enter a commit message"
git subtree pull --prefix langworld_db_data https://github.com/jazyki-mira/langworld_db_data/ master --squash

echo "Re-populating the database"
pipenv run initialize_langworld_db_pyramid_db config/production.ini

echo "Done. Make sure you push the updated tree to remote repository."
