import zope.sqlalchemy
from sqlalchemy import engine_from_config
from sqlalchemy.orm import configure_mappers, sessionmaker

# Import or define all models here to ensure they are attached to the
# ``Base.metadata`` prior to any initialization routines.
from langworld_db_pyramid.models.association_tables import (
    DoculectToFeatureValue,
    DoculectToGlottocode,
    DoculectToIso639P3Code,
)
from langworld_db_pyramid.models.country import Country
from langworld_db_pyramid.models.doculect import Doculect
from langworld_db_pyramid.models.doculect_feature_value_info import DoculectFeatureValueInfo
from langworld_db_pyramid.models.doculect_type import DoculectType
from langworld_db_pyramid.models.encyclopedia_map import EncyclopediaMap
from langworld_db_pyramid.models.encyclopedia_volume import EncyclopediaVolume
from langworld_db_pyramid.models.family import Family
from langworld_db_pyramid.models.feature import Feature
from langworld_db_pyramid.models.feature_category import FeatureCategory
from langworld_db_pyramid.models.feature_value import FeatureValue
from langworld_db_pyramid.models.feature_value_type import FeatureValueType
from langworld_db_pyramid.models.glottocode import Glottocode
from langworld_db_pyramid.models.iso_639p3_code import Iso639P3Code
from langworld_db_pyramid.models.wals_code import WalsCode

# for mypy
__all__ = [
    "DoculectToFeatureValue",
    "DoculectToGlottocode",
    "DoculectToIso639P3Code",
    "DoculectToWalsCode",
    "Country",
    "Doculect",
    "DoculectFeatureValueInfo",
    "DoculectType",
    "EncyclopediaMap",
    "EncyclopediaVolume",
    "Family",
    "Feature",
    "FeatureCategory",
    "FeatureValue",
    "FeatureValueType",
    "Glottocode",
    "Iso639P3Code",
    "WalsCode",
]


# Run ``configure_mappers`` after defining all of the models to ensure
# all relationships can be setup.
configure_mappers()


def get_engine(settings, prefix="sqlalchemy."):  # type: ignore[no-untyped-def]
    return engine_from_config(settings, prefix)


def get_session_factory(engine):  # type: ignore[no-untyped-def]
    factory = sessionmaker()
    factory.configure(bind=engine)
    return factory


def get_tm_session(  # type: ignore[no-untyped-def]
    session_factory, transaction_manager, request=None
):
    """
    Get a ``sqlalchemy.orm.Session`` instance backed by a transaction.

    This function will hook the session to the transaction manager which
    will take care of committing any changes.

    - When using pyramid_tm it will automatically be committed or aborted
      depending on whether an exception is raised.

    - When using scripts you should wrap the session in a manager yourself.
      For example:

      .. code-block:: python

          import transaction

          engine = get_engine(settings)
          session_factory = get_session_factory(engine)
          with transaction.manager:
              dbsession = get_tm_session(session_factory, transaction.manager)

    This function may be invoked with a ``request`` kwarg, such as when invoked
    by the reified ``.dbsession`` Pyramid request attribute which is configured
    via the ``includeme`` function below. The default value, for backwards
    compatibility, is ``None``.

    The ``request`` kwarg is used to populate the ``sqlalchemy.orm.Session``'s
    "info" dict.  The "info" dict is the official namespace for developers to
    stash session-specific information.  For more information, please see the
    SQLAlchemy docs:
    https://docs.sqlalchemy.org/en/stable/orm/session_api.html#sqlalchemy.orm.session.Session.params.info

    By placing the active ``request`` in the "info" dict, developers will be
    able to access the active Pyramid request from an instance of an SQLAlchemy
    object in one of two ways:

    - Classic SQLAlchemy. This uses the ``Session``'s utility class method:

      .. code-block:: python

          from sqlalchemy.orm.session import Session as sa_Session

          dbsession = sa_Session.object_session(dbObject)
          request = dbsession.info["request"]

    - Modern SQLAlchemy. This uses the "Runtime Inspection API":

      .. code-block:: python

          from sqlalchemy import inspect as sa_inspect

          dbsession = sa_inspect(dbObject).session
          request = dbsession.info["request"]
    """
    dbsession = session_factory(info={"request": request})
    zope.sqlalchemy.register(dbsession, transaction_manager=transaction_manager)
    return dbsession


def includeme(config):  # type: ignore[no-untyped-def]
    """
    Initialize the model for a Pyramid app.

    Activate this setup using ``config.include('sqla_demo.models')``.

    """
    settings = config.get_settings()
    settings["tm.manager_hook"] = "pyramid_tm.explicit_manager"

    # Use ``pyramid_tm`` to hook the transaction lifecycle to the request.
    # Note: the packages ``pyramid_tm`` and ``transaction`` work together to
    # automatically close the active database session after every request.
    # If your project migrates away from ``pyramid_tm``, you may need to use a
    # Pyramid callback function to close the database session after each
    # request.
    config.include("pyramid_tm")

    # use pyramid_retry to retry a request when transient exceptions occur
    config.include("pyramid_retry")

    # hook to share the dbengine fixture in testing
    dbengine = settings.get("dbengine")
    if not dbengine:
        dbengine = get_engine(settings)

    session_factory = get_session_factory(dbengine)
    config.registry["dbsession_factory"] = session_factory

    # make request.dbsession available for use in Pyramid
    def dbsession(request):  # type: ignore[no-untyped-def]
        # hook to share the dbsession fixture in testing
        dbsession = request.environ.get("app.dbsession")
        if dbsession is None:
            # request.tm is the transaction manager used by pyramid_tm
            dbsession = get_tm_session(session_factory, request.tm, request=request)
        return dbsession

    config.add_request_method(dbsession, reify=True)
