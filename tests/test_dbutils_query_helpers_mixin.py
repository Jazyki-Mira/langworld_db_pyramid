import pytest
from pyramid.httpexceptions import HTTPNotFound
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult
from sqlalchemy.exc import MultipleResultsFound

from langworld_db_pyramid import models
from langworld_db_pyramid.dbutils.query_helpers import _get, _get_by_man_id, _get_one, get_all
from tests.test_views import NUMBER_OF_TEST_DOCULECTS_WITH_FEATURE_PROFILES


def test__get(dummy_request, setup_models_once_for_test_module):
    stmt = select(models.Doculect).where(models.Doculect.has_feature_profile)
    assert isinstance(_get(dummy_request, stmt), ScalarResult)


def test__get_one(dummy_request, setup_models_once_for_test_module):
    doculect = _get_one(
        dummy_request, select(models.Doculect).where(models.Doculect.man_id == "french")
    )
    assert isinstance(doculect, models.Doculect)


def test__get_one_crashes_when_multiple_results_are_returned(
    dummy_request, setup_models_once_for_test_module
):
    with pytest.raises(MultipleResultsFound):
        _get_one(dummy_request, select(models.Doculect))


def test_get_all(dummy_request, setup_models_once_for_test_module):
    stmt = select(models.Doculect).where(models.Doculect.has_feature_profile)
    data = get_all(dummy_request, stmt)

    assert len(data) == NUMBER_OF_TEST_DOCULECTS_WITH_FEATURE_PROFILES
    for item in data:
        assert isinstance(item, models.Doculect)


def test__get_by_man_id(dummy_request, setup_models_once_for_test_module):
    # I don't think I have to test non-existent ID because user cannot enter it manually.
    family = _get_by_man_id(dummy_request, models.Family, "old_turk")
    assert isinstance(family, models.Family)
    assert family.name_en == "Old Turkic"


def test__get_by_man_id_raises_http_not_found_on_non_existent_man_id(
    dummy_request, setup_models_once_for_test_module
):
    with pytest.raises(HTTPNotFound):
        _get_by_man_id(dummy_request, models.Doculect, "foo")


def test__get_by_man_id_crashes_on_wrong_model(dummy_request, setup_models_once_for_test_module):
    # It is OK for the app to crash because it would be my obvious coding mistake
    # if I pass a model that has no .man_id attribute
    with pytest.raises(AttributeError):
        _get_by_man_id(dummy_request, models.Glottocode, "foo")


def test_query_mixin_get_by_man_id_with_doculect(dummy_request, setup_models_once_for_test_module):
    doculect = models.Doculect.get_by_man_id(dummy_request, "french")
    assert isinstance(doculect, models.Doculect)
    assert doculect.name_en == "French"


def test_query_mixin_get_by_man_id_with_family(dummy_request, setup_models_once_for_test_module):
    family = models.Family.get_by_man_id(dummy_request, "slav")
    assert isinstance(family, models.Family)
    assert family.name_en == "Slavic"


def test_query_mixin_get_by_man_id_with_feature(dummy_request, setup_models_once_for_test_module):
    feature = models.Feature.get_by_man_id(dummy_request, "A-10")
    assert isinstance(feature, models.Feature)
    assert feature.name_en == "Types of diphthongs"


def test_query_mixin_get_by_man_id_with_feature_value(
    dummy_request, setup_models_once_for_test_module
):
    value = models.FeatureValue.get_by_man_id(dummy_request, "K-11-4")
    assert isinstance(value, models.FeatureValue)
    assert value.name_en == "Case"
