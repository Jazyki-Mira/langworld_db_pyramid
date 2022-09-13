import os

import alembic
import alembic.config
import alembic.command
from pathlib import Path
from pyramid.paster import get_appsettings
from pyramid.scripting import prepare
from pyramid.testing import DummyRequest, testConfig
import pytest
import transaction
import webtest

from langworld_db_pyramid import main
from langworld_db_pyramid import models
from langworld_db_pyramid.models.meta import Base
from langworld_db_pyramid.routes import add_routes_for_page_views_with_i18n
# added by me
import tests.paths as paths


def pytest_addoption(parser):
    parser.addoption('--ini', action='store', metavar='INI_FILE')


@pytest.fixture(scope='session')
def ini_file(request):
    # potentially grab this path from a pytest option
    return os.path.abspath(request.config.option.ini or str(Path('config') / 'testing.ini'))


@pytest.fixture(scope='session')
def app_settings(ini_file):
    return get_appsettings(ini_file)


@pytest.fixture(scope='session')
def dbengine(app_settings, ini_file):
    engine = models.get_engine(app_settings)

    alembic_cfg = alembic.config.Config(ini_file)
    Base.metadata.drop_all(bind=engine)
    # noinspection PyTypeChecker
    alembic.command.stamp(alembic_cfg, None, purge=True)

    # run migrations to initialize the database
    # depending on how we want to initialize the database from scratch
    # we could alternatively call:
    # Base.metadata.create_all(bind=engine)
    # alembic.command.stamp(alembic_cfg, "head")
    alembic.command.upgrade(alembic_cfg, "head")

    yield engine

    Base.metadata.drop_all(bind=engine)
    # noinspection PyTypeChecker
    alembic.command.stamp(alembic_cfg, None, purge=True)


@pytest.fixture(scope='session')
def app(app_settings, dbengine):
    return main({}, dbengine=dbengine, **app_settings)


@pytest.fixture(scope='module')
def tm():
    tm = transaction.TransactionManager(explicit=True)
    tm.begin()
    tm.doom()

    yield tm

    tm.abort()


@pytest.fixture(scope='module')
def dbsession(app, tm):
    session_factory = app.registry['dbsession_factory']
    return models.get_tm_session(session_factory, tm)


@pytest.fixture
def testapp(app, tm, dbsession):
    # override request.dbsession and request.tm with our own
    # externally-controlled values that are shared across requests but aborted
    # at the end
    testapp = webtest.TestApp(app,
                              extra_environ={
                                  'HTTP_HOST': 'example.com',
                                  'tm.active': True,
                                  'tm.manager': tm,
                                  'app.dbsession': dbsession,
                              })

    return testapp


@pytest.fixture
def app_request(app, tm, dbsession):
    """
    A real request.

    This request is almost identical to a real request but it has some
    drawbacks in tests as it's harder to mock data and is heavier.

    """
    with prepare(registry=app.registry) as env:
        request = env['request']
        request.host = 'example.com'

        # without this, request.dbsession will be joined to the same transaction
        # manager but it will be using a different sqlalchemy.orm.Session using
        # a separate database transaction
        request.dbsession = dbsession
        request.tm = tm

        yield request


@pytest.fixture
def dummy_request(tm, dbsession):
    """
    A lightweight dummy request.

    This request is ultra-lightweight and should be used only when the request
    itself is not a large focus in the call-stack.  It is much easier to mock
    and control side-effects using this object, however:

    - It does not have request extensions applied.
    - Threadlocals are not properly pushed.

    """
    request = DummyRequest()
    request.host = 'example.com'
    request.dbsession = dbsession
    request.tm = tm

    return request


@pytest.fixture
def dummy_config(dummy_request):
    """
    A dummy :class:`pyramid.config.Configurator` object.  This allows for
    mock configuration, including configuration for ``dummy_request``, as well
    as pushing the appropriate threadlocals.

    """
    with testConfig(request=dummy_request) as config:
        add_routes_for_page_views_with_i18n(config)
        yield config


# Fixtures added by me
PATHS_FOR_DB_INITIALIZER = {
    'dir_with_feature_profiles': paths.DIR_WITH_FEATURE_PROFILES_FOR_INITIALIZE_DB,
    'file_with_categories': paths.FILE_WITH_CATEGORIES_FOR_INITIALIZE_DB,
    'file_with_countries': paths.FILE_WITH_COUNTRIES_FOR_INITIALIZE_DB,
    'file_with_doculects': paths.FILE_WITH_DOCULECTS_FOR_INITIALIZE_DB,
    'file_with_encyclopedia_maps': paths.FILE_WITH_MAPS_FOR_INITIALIZE_DB,
    'file_with_encyclopedia_map_to_doculect': paths.FILE_WITH_MAP_TO_DOCULECT_FOR_INITIALIZE_DB,
    'file_with_encyclopedia_volumes': paths.FILE_WITH_ENCYCLOPEDIA_VOLUMES_FOR_INITIALIZE_DB,
    'file_with_genealogy_hierarchy': paths.FILE_WITH_GENEALOGY_HIERARCHY_FOR_INITIALIZE_DB,
    'file_with_genealogy_names': paths.FILE_WITH_GENEALOGY_NAMES_FOR_INITIALIZE_DB,
    'file_with_listed_values': paths.FILE_WITH_LISTED_VALUES_FOR_INITIALIZE_DB,
    'file_with_names_of_features': paths.FILE_WITH_FEATURES_FOR_INITIALIZE_DB,
    'file_with_value_types': paths.FILE_WITH_VALUE_TYPES_FOR_INITIALIZE_DB,
}


@pytest.fixture
def test_db_initializer(dbsession):

    from langworld_db_pyramid.scripts.initialize_db import CustomModelInitializer
    return CustomModelInitializer(dbsession=dbsession, **PATHS_FOR_DB_INITIALIZER)


@pytest.fixture(scope='module')
def test_db_initializer_with_module_scope(dbsession):

    from langworld_db_pyramid.scripts.initialize_db import CustomModelInitializer
    return CustomModelInitializer(dbsession=dbsession, **PATHS_FOR_DB_INITIALIZER)


@pytest.fixture(scope='module')
def setup_models_once_for_test_module(test_db_initializer_with_module_scope):
    test_db_initializer_with_module_scope.setup_models()
