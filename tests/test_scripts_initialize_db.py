from sqlalchemy import select

from langworld_db_data.tools.files.csv_xls import read_dicts_from_csv
from langworld_db_pyramid import models


class TestCustomModelInitializer:
    def test_setup_models(self, dbsession, test_db_initializer):
        # dbsession and test_initializer.dbsession is the same object
        # since the dummy dbsession is passed to constructor or CustomModelInitializer

        NUMBER_OF_FEATURES = 129
        # EXPECTED NUMBER OF VALUES IN FeatureValue TABLE
        number_of_listed_values = 1219
        number_of_compound_listed_values = 28
        number_of_empty_values = NUMBER_OF_FEATURES * 3  # 3 value types with empty values

        unique_custom_values = set()
        for file in test_db_initializer.dir_with_feature_profiles.glob("*.csv"):
            rows_with_custom_values = {
                # comment not included because FeatureValue table contains values without comments
                (row["feature_id"], row["value_ru"])
                for row in read_dicts_from_csv(file)
                if row["value_type"] == "custom"
            }
            unique_custom_values.update(rows_with_custom_values)

        test_db_initializer.setup_models()

        # TODO create functions that read CSV files and check?
        #  Otherwise it's not very reliable where I can't check
        #  number of items manually.
        expected_number_of_items_for_model = {
            models.Country: 283,
            models.Doculect: 438,
            models.DoculectType: 3,
            models.EncyclopediaMap: 62,
            models.EncyclopediaVolume: 21,
            models.Family: 145,
            models.Feature: NUMBER_OF_FEATURES,
            models.FeatureCategory: 14,
            models.FeatureValue: number_of_listed_values
            + number_of_empty_values
            + number_of_compound_listed_values
            + len(unique_custom_values),
            models.FeatureValueType: 5,
            models.Glottocode: 441,
            models.Iso639P3Code: 418,
            models.WalsCode: 271,
        }

        for model in expected_number_of_items_for_model:
            all_items = dbsession.scalars(select(model)).all()
            assert len(list(all_items)) == expected_number_of_items_for_model[model]

        all_doculects = dbsession.scalars(select(models.Doculect)).all()

        assert len([d for d in all_doculects if d.has_feature_profile]) == len(
            list(test_db_initializer.dir_with_feature_profiles.glob("*.csv"))
        )

        for item in all_doculects:
            assert item.man_id
            assert isinstance(item.main_country, models.Country)
            assert isinstance(item.type, models.DoculectType)

            if item.encyclopedia_volume_id:
                assert isinstance(item.encyclopedia_volume, models.EncyclopediaVolume)
            if item.has_feature_profile:
                # With multi-select features, there can be more values than there are features:
                # For each element of a compound value, a separate line in the table is created.
                assert len(item.feature_values) >= NUMBER_OF_FEATURES

        afg = dbsession.scalars(
            select(models.Country).where(models.Country.name_en == "Afghanistan")
        ).one()
        assert len(afg.doculects) == 23

        rom_volume = dbsession.scalars(
            select(models.EncyclopediaVolume).where(models.EncyclopediaVolume.id == "11")
        ).one()
        assert len(rom_volume.doculects) == 24

        # family top to bottom
        mande = dbsession.scalars(
            select(models.Family).where(models.Family.man_id == "mande")
        ).one()
        assert len(mande.children) == 2
        western = mande.children[0]
        assert western.name_ru == "Западные"
        assert len(western.children) == 6
        manding = western.children[0]
        assert len(manding.children) == 2
        assert manding.children[1].name_en == "Manding-East"

        # family bottom to top
        yupik = dbsession.scalars(
            select(models.Family).where(models.Family.man_id == "yupik")
        ).one()
        assert yupik.parent.name_en == "Eskimo"
        assert yupik.parent.parent.name_ru == "Эскимосско-алеутские"

        # relationship between family and doculects
        east_rom = dbsession.scalars(
            select(models.Family).where(models.Family.man_id == "east_rom")
        ).one()
        assert len(east_rom.doculects) == 4
        for doculect in east_rom.doculects:
            assert doculect.name_en in (
                "Aromanian",
                "Istro-Rumanian",
                "Megleno-Romanian",
                "Romanian",
            )

        # random check of different attributes of a doculect
        old_russian: models.Doculect = dbsession.scalars(
            select(models.Doculect).where(models.Doculect.name_en == "Old Russian")
        ).one()
        assert old_russian.family.name_en == "East Slavic"
        assert old_russian.family.parent.name_en == "Slavic"
        assert old_russian.family.parent.parent.name_ru == "Индоевропейские"
        assert len(old_russian.encyclopedia_maps) == 2
        assert "13-2" in [map_.man_id for map_ in old_russian.encyclopedia_maps]
        assert "13-11" in [map_.man_id for map_ in old_russian.encyclopedia_maps]
        assert "Ruthenian" in old_russian.aliases_en
        assert len(old_russian.iso_639p3_codes) == len(old_russian.glottocodes) == 1
        assert "orv" in [code.code for code in old_russian.iso_639p3_codes]
        assert "oldr1238" in [code.code for code in old_russian.glottocodes]
        assert old_russian.main_country.name_en == "Ukraine"
        assert old_russian.encyclopedia_volume.id == "13"
        assert old_russian.page == "449"
        assert old_russian.has_feature_profile
        assert "A-9-2" in [value.man_id for value in old_russian.feature_values]
        assert "A-10-1" not in [value.man_id for value in old_russian.feature_values]

        # `is_listed_and_has_doculects` attribute in non-listed feature values must be False
        for non_listed_value in dbsession.scalars(
            select(models.FeatureValue).where(models.FeatureValue.man_id == "")
        ).all():
            assert not non_listed_value.is_listed_and_has_doculects

        # checking `is_listed_and_has_doculects` attribute in listed feature values
        a31 = dbsession.scalars(
            select(models.FeatureValue).where(models.FeatureValue.man_id == "A-3-1")
        ).one()
        assert not a31.is_listed_and_has_doculects
        a32 = dbsession.scalars(
            select(models.FeatureValue).where(models.FeatureValue.man_id == "A-3-2")
        ).one()
        assert a32.is_listed_and_has_doculects

        # checking elements and compounds
        compound_id = "K-15-4|K-15-2|K-15-3|K-15-8"
        compound = dbsession.scalars(
            select(models.FeatureValue).where(models.FeatureValue.man_id == compound_id)
        ).one()
        assert len(compound.elements) == len(
            compound_id.split(models.feature_value.COMPOUND_VALUE_DELIMITER)
        )
        k15_4 = dbsession.scalars(
            select(models.FeatureValue).where(models.FeatureValue.man_id == "K-15-4")
        ).one()
        assert compound in k15_4.compounds

        # checking compound value and its elements in a doculect
        amharic: models.Doculect = dbsession.scalars(
            select(models.Doculect).where(models.Doculect.name_en == "Amharic")
        ).one()
        for value_id in ("K-15-4|K-15-2|K-15-3|K-15-8", "K-15-4", "K-15-2", "K-15-3", "K-15-8"):
            assert value_id in [value.man_id for value in amharic.feature_values]

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

    afg = dbsession.scalars(
        select(models.Country).where(models.Country.name_en == "Afghanistan")
    ).one()
    assert len(afg.doculects) > 10

    rom_volume = dbsession.scalars(
        select(models.EncyclopediaVolume).where(models.EncyclopediaVolume.id == "11")
    ).one()
    assert len(rom_volume.doculects) > 20
