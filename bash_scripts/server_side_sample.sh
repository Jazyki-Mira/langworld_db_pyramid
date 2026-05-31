#!/bin/bash

# Deployment script: pulls latest code, installs dependencies, compiles localization, restarts service

# strict mode: make sure errors don't pass silently
set -euo pipefail

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd ${SCRIPT_DIR}/../

git fetch origin
git reset --hard origin/master

pip install pipenv
pipenv install

${SCRIPT_DIR}/init_compile.sh

# Restart the systemd service to apply changes
# Note: assumes a systemd service called 'langworld.service' was created during VPS setup
sudo systemctl restart langworld.service

# Display service status to confirm successful restart
sudo systemctl status langworld.service --no-pager
