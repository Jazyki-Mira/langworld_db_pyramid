import pytest
from sqlalchemy import select

import langworld_db_pyramid.models as models
from tests.paths import *


@pytest.fixture
def test_initializer(dbsession):
    from langworld_db_pyramid.scripts.initialize_db import CustomModelInitializer
    return CustomModelInitializer(
        dbsession=dbsession,
        dir_with_feature_profiles=DIR_WITH_FEATURE_PROFILES_FOR_INITIALIZE_DB,
        file_with_categories=FILE_WITH_CATEGORIES_FOR_INITIALIZE_DB,
        file_with_countries=FILE_WITH_COUNTRIES_FOR_INITIALIZE_DB,
        file_with_doculects=FILE_WITH_DOCULECTS_FOR_INITIALIZE_DB,
        file_with_encyclopedia_volumes=FILE_WITH_ENCYCLOPEDIA_VOLUMES_FOR_INITIALIZE_DB,
        file_with_listed_values=FILE_WITH_LISTED_VALUES_FOR_INITIALIZE_DB,
        file_with_names_of_features=FILE_WITH_FEATURES_FOR_INITIALIZE_DB,
        file_with_value_types=FILE_WITH_VALUE_TYPES_FOR_INITIALIZE_DB,
    )


class TestCustomModelInitializer:
    def test_setup_models(self, dbsession, test_initializer):
        # dbsession and test_initializer.dbsession is the same object
        # since the dummy dbsession is passed to constructor or CustomModelInitializer

        test_initializer.setup_models()

        all_doculects = dbsession.scalars(select(models.Doculect)).all()
        assert len(list(all_doculects)) == 429

        all_countries = dbsession.scalars(select(models.Country)).all()
        assert len(all_countries) == 283

        for item in all_doculects:
            assert item.man_id
            assert isinstance(item.main_country, models.Country)
            assert item.main_country.id

        afg = dbsession.scalars(select(models.Country).where(models.Country.name_en == 'Afghanistan')).one()
        assert len(afg.doculects) == 21

        rom_volume = dbsession.scalars(select(models.EncyclopediaVolume).where(models.EncyclopediaVolume.id == '11')).one()
        assert len(rom_volume.doculects) == 24


def test_initialize_db_with_real_data(dbsession):
    """Test with real data. Checks are not so precise
    to avoid changing them every time real data changes.

    Precise checks are done with test data.
    """
    from langworld_db_pyramid.scripts.initialize_db import setup_models

    setup_models(dbsession)

    all_doculects = dbsession.scalars(select(models.Doculect)).all()
    assert len(list(all_doculects)) > 400

    all_countries = dbsession.scalars(select(models.Country)).all()
    assert len(all_countries) > 200

    for item in all_doculects:
        assert item.man_id
        assert isinstance(item.main_country, models.Country)
        assert item.main_country.id

    afg = dbsession.scalars(select(models.Country).where(models.Country.name_en == 'Afghanistan')).one()
    assert len(afg.doculects) > 10

    rom_volume = dbsession.scalars(select(models.EncyclopediaVolume).where(models.EncyclopediaVolume.id == '11')).one()
    assert len(rom_volume.doculects) > 20
