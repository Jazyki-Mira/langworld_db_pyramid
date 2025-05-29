# Bash scripts

## For development
- [`init_compile.sh`](init_compile.sh) populates the database and compiles `Babel` message catalog (for i18n).
- [`pull_data.sh`](pull_data.sh) downloads data files from the [data repository](https://github.com/lemontree210/langworld_db_data/) with `git subtree`, merges changes into `master` (note that an editor for a commit message will pop up) and re-populates the SQL database. This script does **not** automatically push the changes to remote repository of `langworld_db_pyramid` (this project). Do that when you're ready.

## For running on the web server
- [`server_side_sample.sh`](server_side_sample.sh) pulls `langworld_db_pyramid` from GitHub, populates the SQL database, compiles `Babel` message catalog for i18n. **This script is a sample** - copy it to `server_side.sh` and modify it to fit particular requirements of your server. For example, PythonAnywhere may not support pipenv and you will need to modify the script to temporarily create requirements.txt file and use `pip` instead of `pipenv`.
