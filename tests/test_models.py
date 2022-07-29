import pytest
from sqlalchemy import select

import langworld_db_pyramid.models as models


@pytest.mark.parametrize(
    'man_id, expected_result',
    [
        ('ital', True), ('slav', True), ('east_slav', True), ('isolate', True),
        ('inuit', False)  # there are doculects in doculects.csv, but they have no feature profiles
    ]
)
def test_family_has_doculects_with_feature_profiles(
        dbsession, setup_models_for_views_testing, man_id, expected_result
):
    family = dbsession.scalars(select(models.Family).where(models.Family.man_id == man_id)).one()
    assert family.has_doculects_with_feature_profiles() == expected_result


@pytest.mark.parametrize(
    'man_id, expected_doculect_ids',
    [
        ('east_rom', ['aromanian', 'istro_romanian', 'megleno_romanian', 'romanian']),
        ('north_sem', [
            'ancient_hebrew', 'modern_hebrew', 'phoenician', 'neo_aramaic_of_maalula',
            'neo_mandaic', 'turoyo', 'official_aramaic', 'jewish_palestinian_aramaic',
            'classical_mandaic', 'classical_syriac', 'ugaritic'
        ]),  # ugaritic is a top-level doculect, others are doculects in subfamilies (included nested ones)
        ('inuit', [])
    ]
)
def test_family_iter_doculects_that_have_feature_profiles(
        dbsession, setup_models_for_views_testing, man_id, expected_doculect_ids
):
    family = dbsession.scalars(select(models.Family).where(models.Family.man_id == man_id)).one()
    ids = [d.man_id for d in family.iter_doculects_that_have_feature_profiles()]
    assert sorted(ids) == sorted(expected_doculect_ids)