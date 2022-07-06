import pytest

from langworld_db_pyramid.models.doculect import Doculect
from langworld_db_pyramid.views.doculects_list import view_all_doculects, view_doculect_profile
from langworld_db_pyramid.views.json_api import get_man_ids_of_doculects_containing_substring
from langworld_db_pyramid.views.notfound import notfound_view


@pytest.mark.parametrize(
    'query, locale, expected_items',
    [
        ('dut', 'en', ('afrikaans', 'dutch')),  # 'dut' is in aliases for Afrikaans and in main name for Dutch
        # the request is in Russian but IDs received are English:
        ('немец', 'ru', ('dutch', 'german', 'luxembourgian', 'swiss_german', 'yiddish'))
    ]

)
def test_sample_json_view(
        dummy_request, setup_models_for_views_testing,
        query, locale, expected_items,
):

    dummy_request.matchdict['locale'] = locale
    dummy_request.matchdict['query'] = query

    data = get_man_ids_of_doculects_containing_substring(dummy_request)

    assert len(data) == len(expected_items)

    for item in expected_items:
        assert item in data


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
