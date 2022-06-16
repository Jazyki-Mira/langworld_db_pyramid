import logging

from sqlalchemy import select

import langworld_db_pyramid.models as models


def test_initialize_db(dbsession):
    from langworld_db_pyramid.scripts.initialize_db import setup_models

    setup_models(dbsession)

    all_doculects = dbsession.scalars(select(models.Doculect)).all()
    assert len(list(all_doculects)) == 429

    all_countries = dbsession.scalars(select(models.Country)).all()
    assert len(all_countries) == 283

    for item in all_doculects:
        assert item.string_id
        assert isinstance(item.main_country, models.Country)
        assert item.main_country.id
        # print(item.main_country.id, item.main_country.man_id)

    afg = dbsession.scalars(select(models.Country).where(models.Country.name_en == 'Afghanistan')).one()
    assert len(afg.doculects) == 21

