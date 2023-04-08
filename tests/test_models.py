import pytest
from sqlalchemy import select

from langworld_db_pyramid import models


class TestDoculect:
    @pytest.mark.parametrize(
        "man_id, expected_result",
        [
            ("east_rom", True),  # immediate family
            ("rom", True),
            ("ital", True),
            ("indo_euro", True),  # going up the tree
            ("balk_rom", False),  # child of east_rom
            ("italo_west", False),
            ("celt", False),
            ("inuit", False),
        ],
    )
    def test_doculect_belongs_to_family(
        self, dbsession, setup_models_once_for_test_module, man_id, expected_result
    ):
        romanian = dbsession.scalars(
            select(models.Doculect).where(models.Doculect.man_id == "romanian")
        ).one()
        assert romanian.belongs_to_family(man_id) == expected_result


class TestFamily:
    @pytest.mark.parametrize(
        "man_id, expected_result",
        [
            ("ital", True),
            ("slav", True),
            ("east_slav", True),
            ("isolate", True),
            (
                "inuit",
                False,
            ),  # there are doculects in doculects.csv, but they have no feature profiles
        ],
    )
    def test_family_has_doculects_with_feature_profiles(
        self, dbsession, setup_models_once_for_test_module, man_id, expected_result
    ):
        family = dbsession.scalars(
            select(models.Family).where(models.Family.man_id == man_id)
        ).one()
        assert family.has_doculects_with_feature_profiles() == expected_result

    @pytest.mark.parametrize(
        "man_id_of_presumable_parent, expected_result",
        [
            ("rom", True),  # immediate parent
            ("ital", True),  # grandparent
            ("indo_euro", True),  # great-grandparent
            ("balk_rom", False),  # family is not a descendant of its child
            ("east_rom", False),  # family is not a descendant of itself
            ("isolate", False),
            ("inuit", False),
        ],
    )
    def test_family_is_descendant_of(
        self,
        dbsession,
        setup_models_once_for_test_module,
        man_id_of_presumable_parent,
        expected_result,
    ):
        east_romance = dbsession.scalars(
            select(models.Family).where(models.Family.man_id == "east_rom")
        ).one()
        assert east_romance.is_descendant_of(man_id_of_presumable_parent) == expected_result

    @pytest.mark.parametrize(
        "man_id, expected_doculect_ids",
        [
            ("east_rom", ["aromanian", "istro_romanian", "megleno_romanian", "romanian"]),
            (
                "north_sem",
                [
                    "ancient_hebrew",
                    "modern_hebrew",
                    "phoenician",
                    "neo_aramaic_of_maalula",
                    "neo_mandaic",
                    "turoyo",
                    "official_aramaic",
                    "jewish_palestinian_aramaic",
                    "classical_mandaic",
                    "classical_syriac",
                    "ugaritic",
                ],
            ),  # ugaritic is a top-level doculect, others are doculects in subfamilies (included nested ones)
            ("inuit", []),
        ],
    )
    def test_family_iter_doculects_that_have_feature_profiles(
        self, dbsession, setup_models_once_for_test_module, man_id, expected_doculect_ids
    ):
        family = dbsession.scalars(
            select(models.Family).where(models.Family.man_id == man_id)
        ).one()
        ids = [d.man_id for d in family.iter_doculects_that_have_feature_profiles()]
        assert sorted(ids) == sorted(expected_doculect_ids)
