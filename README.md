# Jazyki Mira (Languages of the World) online database

Jazyki Mira (Languages of the World) Database as a [Pyramid](https://trypyramid.com/) web app.

The data is pulled with `git subtree` from a
data repository into [*langworld_db_data*](langworld_db_data). The actual data files are in [*data*](langworld_db_data/data) subdirectory of that package.
See the [Entity Relationship Diagram](langworld_db_pyramid/dbutils/erd.png) of the relational database that was generated from the data for the web app.

The [*langworld_db_pyramid*](langworld_db_pyramid)
package contains the actual Pyramid web app. The tests
for this package are stored in a [separate directory](tests).

## Installation

### Prerequisites
- Python 3.9
- `pipenv` (see [pipenv docs](https://pipenv-fork.readthedocs.io/en/latest/install.html#installing-pipenv) for details)

### Clone repository (and `cd` into package directory)

```bash
git clone https://github.com/lemontree210/langworld_db_pyramid/; cd langworld_db_pyramid
```

### Copy default [PasteDeploy](https://pastedeploy.readthedocs.io/en/latest/index.html) `.ini` files and edit them if necessary

Copy `.ini` files from [`/config/default/`](config/default) to [`/config/`](config). Edit if necessary (e.g. `sqlalchemy.url` for the database). 

One thing that is missing there and **must** be entered is a [MapBox](https://www.mapbox.com/) token 
(`mapbox_access_token` key in `[app:main]` section).

No `.ini` files in [`/config/`](config) directory will be checked into VCS
(as per [`.gitignore`](.gitignore)).

### Create a virtual environment and install dependencies (from [`Pipfile`](Pipfile))

```bash
pipenv install
```

_Note #1: This will also automatically install `langworld_db_pyramid`  and `langworld_db_data` packages locally as they are mentioned in [`Pipfile`](Pipfile). 
There is no need to manually run `pip install -e .` (from [Pyramid docs](https://docs.pylonsproject.org/projects/pyramid/en/2.0-branch/narr/project.html#installing-your-newly-created-project-for-development)) separately._ 

_Note #2: These two packages will be installed in editable mode, which conforms to upcoming `pip` behavior that will install all local packages without copying them to the directory of the virtual environment._

To install with development dependencies (testing, linting):

```bash
pipenv install --dev
```

### Activate or use the virtual environment

Activate virtual environment...

```
pipenv shell
```

...or run all commands with `pipenv run`.


**All commands below must be run under virtual environment.**

### Initialize database

Apply [`alembic` migrations](langworld_db_pyramid/alembic/versions) to the database, then run the [`initialize_db` script](langworld_db_pyramid/scripts/initialize_db.py) that populates the database with data from [`langworld_db_data`](langworld_db_data).

```bash
alembic -c config/production.ini upgrade head; initialize_langworld_db_pyramid_db config/production.ini
```

### Compile message catalog for multilingual support (i18n)

```bash
pybabel compile --directory=langworld_db_pyramid/locale --locale=en
```

## Serve locally ...
```bash
pserve config/production.ini
```

## ... or setup your WSGI server.

I will add some information here as I go.

## Use `development.ini` file in for development

For development, use [`development.ini`](config/development.ini) instead of [`production.ini`](config/production.ini).

Serve locally with `--reload` flag for `waitress` to reflect changes in [views](langworld_db_pyramid/views) and [templates](langworld_db_pyramid/templates) instantly:

```bash
pserve config/development.ini --reload
```

## Run [tests](tests)

```bash
pytest --cov
```
(works only if the project was installed in development mode)