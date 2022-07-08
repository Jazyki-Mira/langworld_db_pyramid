from sqlalchemy import select

from langworld_db_data.langworld_db_data.filetools.csv_xls import read_csv
import langworld_db_pyramid.models as models


class TestCustomModelInitializer:
    def test_setup_models(self, dbsession, test_db_initializer):
        # dbsession and test_initializer.dbsession is the same object
        # since the dummy dbsession is passed to constructor or CustomModelInitializer

        NUMBER_OF_FEATURES = 126
        # CALCULATING EXPECTED NUMBER OF VALUES IN FeatureValue TABLE
        number_of_listed_values = 1232
        number_of_empty_values = NUMBER_OF_FEATURES * 3  # 3 value types with empty values

        unique_custom_values = set()
        for file in test_db_initializer.dir_with_feature_profiles.glob('*.csv'):
            rows_with_custom_values = {
                # comment not included because FeatureValue table contains values without comments
                (row['feature_id'], row['value_ru'])
                for row in read_csv(file, read_as='dicts') if row['value_type'] == 'custom'
            }
            unique_custom_values.update(rows_with_custom_values)

        test_db_initializer.setup_models()

        expected_number_of_items_for_model = {
            models.Country: 283,
            models.Doculect: 429,
            models.DoculectType: 3,
            models.EncyclopediaVolume: 19,
            models.Family: 145,
            models.Feature: 126,
            models.FeatureCategory: 14,
            models.FeatureValue: number_of_listed_values + number_of_empty_values + len(unique_custom_values),
            models.FeatureValueType: 5,
            models.Glottocode: 427,
            models.Iso639P3Code: 405,
        }

        for model in expected_number_of_items_for_model:
            all_items = dbsession.scalars(select(model)).all()
            assert len(list(all_items)) == expected_number_of_items_for_model[model]

        all_doculects = dbsession.scalars(select(models.Doculect)).all()

        assert len([d for d in all_doculects if d.has_feature_profile]) == \
               len(list(test_db_initializer.dir_with_feature_profiles.glob('*.csv')))

        for item in all_doculects:
            assert item.man_id
            assert isinstance(item.main_country, models.Country)
            assert isinstance(item.type, models.DoculectType)

            if item.encyclopedia_volume_id:
                assert isinstance(item.encyclopedia_volume, models.EncyclopediaVolume)
            if item.has_feature_profile:
                assert len(item.feature_values) == NUMBER_OF_FEATURES

        afg = dbsession.scalars(select(models.Country).where(models.Country.name_en == 'Afghanistan')).one()
        assert len(afg.doculects) == 21

        rom_volume = dbsession.scalars(select(models.EncyclopediaVolume).where(models.EncyclopediaVolume.id == '11')).one()
        assert len(rom_volume.doculects) == 24

        # family top to bottom
        mande = dbsession.scalars(select(models.Family).where(models.Family.man_id == 'mande')).one()
        assert len(mande.children) == 2
        western = mande.children[0]
        assert western.name_ru == 'Западные'
        assert len(western.children) == 6
        manding = western.children[0]
        assert len(manding.children) == 2
        assert manding.children[1].name_en == 'Manding-East'

        # family bottom to top
        yupik = dbsession.scalars(select(models.Family).where(models.Family.man_id == 'yupik')).one()
        assert yupik.parent.name_en == 'Eskimo'
        assert yupik.parent.parent.name_ru == 'Эскимосско-алеутские'

    def test__delete_all_data(self, dbsession, test_db_initializer):
        test_db_initializer.setup_models()

        test_db_initializer._delete_all_data()

        for model in test_db_initializer.ALL_MODELS:
            items = dbsession.scalars(select(model)).all()
            assert not items


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
