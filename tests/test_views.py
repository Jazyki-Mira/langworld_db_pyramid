import pytest

from langworld_db_pyramid.models.doculect import Doculect
from langworld_db_pyramid.views.doculects_list import view_all_doculects
from langworld_db_pyramid.views.doculect_profile import view_doculect_profile
from langworld_db_pyramid.views.json_api import get_doculects_by_substring
from langworld_db_pyramid.views.notfound import notfound_view


@pytest.mark.parametrize(
    'query, locale, expected_ids',
    [
        ('dut', 'en', ('afrikaans', 'dutch')),  # 'dut' is in aliases for Afrikaans and in main name for Dutch
        # the request is in Russian but IDs received are English:
        ('немец', 'ru', ('dutch', 'german', 'luxembourgian', 'swiss_german', 'yiddish'))
    ]

)
def test_get_doculects_by_substring(
        dummy_request, setup_models_for_views_testing,
        query, locale, expected_ids,
):

    dummy_request.matchdict['locale'] = locale
    dummy_request.matchdict['query'] = query

    doculects = get_doculects_by_substring(dummy_request)

    assert len(doculects) == len(expected_ids)

    for doculect in doculects:
        for key in ('id', 'name', 'aliases', 'iso639p3Codes', 'glottocodes'):
            assert key in doculect.keys()

    for doculect_id in expected_ids:
        ids = [doculect['id'] for doculect in doculects]
        assert doculect_id in ids


def test_view_all_doculects_success(dummy_request, setup_models_for_views_testing):

    info = view_all_doculects(dummy_request)
    assert dummy_request.response.status_int == 200
    assert len(info['doculects']) == 429


def test_view_doculect_profile(dummy_request, setup_models_for_views_testing):
    dummy_request.matchdict['doculect_man_id'] = 'aragonese'

    info = view_doculect_profile(dummy_request)
    doculect = info['doculect']
    assert isinstance(doculect, Doculect)
    assert doculect.name_en == 'Aragonese'


def test_notfound_view(dummy_request):
    info = notfound_view(dummy_request)
    assert dummy_request.response.status_int == 404
    assert info == {}
