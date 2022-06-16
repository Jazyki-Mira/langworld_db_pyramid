from sqlalchemy import select

import langworld_db_pyramid.models as models


def test_initialize_db(dbsession):
    from langworld_db_pyramid.scripts.initialize_db import setup_models

    setup_models(dbsession)
    result = dbsession.scalars(select(models.Doculect)).all()

    assert len(list(result)) == 429

    for item in result:
        assert item.string_id
