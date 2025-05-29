from pathlib import Path

from sqlalchemy import select

from langworld_db_data.tools.files.csv_xls import read_dicts_from_csv
from langworld_db_pyramid import models

from .utils.test_data_counter import TestDataCounter

TEST_DATA_DIR = Path(__file__).parent / "test_data" / "initialize_db"


class TestCustomModelInitializer:

    def test_setup_models(self, dbsession, test_db_initializer):
        test_db_initializer.setup_models()
        self._verify_model_counts(dbsession, test_db_initializer)
        self._verify_doculect_properties(dbsession, test_db_initializer)
        self._verify_selected_instances(dbsession, test_db_initializer)

    def _verify_model_counts(self, dbsession, test_db_initializer):
        """Verify that all models have the expected number of items.

        Collects all model count mismatches and raises a single error if any are found.
        """
        counter = TestDataCounter(TEST_DATA_DIR)
        expected_counts = counter.get_expected_model_counts()
        mismatches = []

        for model, expected_count in expected_counts.items():
            actual_count = len(dbsession.scalars(select(model)).all())
            if actual_count != expected_count:
                mismatches.append((model.__name__, expected_count, actual_count))

        if mismatches:
            error_message = "Model count mismatches found:\n" + "\n".join(
                f"{model} (CSV: {expected} vs DB: {actual})"
                for model, expected, actual in mismatches
            )
            raise AssertionError(error_message)

    def _verify_doculect_properties(self, dbsession, test_db_initializer):
        """Verify properties of all doculects in the database."""
        doculects = dbsession.scalars(select(models.Doculect)).all()
        feature_profiles = list(test_db_initializer.dir_with_feature_profiles.glob("*.csv"))

        # Verify number of doculects with feature profiles
        doculects_with_profiles = [d for d in doculects if d.has_feature_profile]
        assert len(doculects_with_profiles) == len(feature_profiles)

        # Verify individual doculect properties
        for doculect in doculects:
            self._verify_single_doculect(doculect)

    def _verify_single_doculect(self, doculect):
        """Verify properties of a single doculect."""
        counter = TestDataCounter(TEST_DATA_DIR)
        assert doculect.man_id
        assert isinstance(doculect.main_country, models.Country)
        assert isinstance(doculect.type, models.DoculectType)

        if doculect.encyclopedia_volume_id:
            assert isinstance(doculect.encyclopedia_volume, models.EncyclopediaVolume)
        if doculect.has_feature_profile:
            assert len(doculect.feature_values) >= counter.count_features()

    def _verify_selected_instances(self, dbsession, test_db_initializer):

        afg = dbsession.scalars(
            select(models.Country).where(models.Country.name_en == "Afghanistan")
        ).one()
        assert len(afg.doculects) == 21, "Expected 21 doculects for Afghanistan"

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
        assert "A-9-1" in [value.man_id for value in old_russian.feature_values]
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
        compound_id = "K-14-4|K-14-5|K-14-6|K-14-7"
        compound = dbsession.scalars(
            select(models.FeatureValue).where(models.FeatureValue.man_id == compound_id)
        ).one()
        assert len(compound.elements) == len(
            compound_id.split(models.feature_value.COMPOUND_VALUE_DELIMITER)
        )
        k14_4 = dbsession.scalars(
            select(models.FeatureValue).where(models.FeatureValue.man_id == "K-14-4")
        ).one()
        assert compound in k14_4.compounds

        # checking compound value and its elements in a doculect
        amharic: models.Doculect = dbsession.scalars(
            select(models.Doculect).where(models.Doculect.name_en == "Amharic")
        ).one()
        for value_id in ("K-14-4|K-14-5|K-14-6|K-14-7", "K-14-4", "K-14-5", "K-14-6", "K-14-7"):
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
