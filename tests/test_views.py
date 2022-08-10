import pyramid.httpexceptions
import pytest

from langworld_db_pyramid.models.doculect import Doculect
from langworld_db_pyramid.models.family import Family
from langworld_db_pyramid.models.feature_category import FeatureCategory
from langworld_db_pyramid.views.doculects_list import get_doculects_by_substring, view_all_doculects_list
from langworld_db_pyramid.views.doculects_map import get_doculects_for_map
from langworld_db_pyramid.views.doculect_profile import view_doculect_profile
from langworld_db_pyramid.views.families import (
    get_parent_families_icons,
    MATCHDICT_ID_FOR_ALL_FAMILIES,
    view_families_for_list,
    view_families_for_map
)
from langworld_db_pyramid.views.features import (
    get_feature_values_icons,
    view_all_features_list_by_category,
    view_feature_list_of_values,
    view_feature_map_of_values
)
from langworld_db_pyramid.views.notfound import notfound_view
from langworld_db_pyramid.views.query_wizard import get_matching_doculects

NUMBER_OF_TEST_DOCULECTS_WITH_FEATURE_PROFILES = 338  # only those (out of 429) that have has_feature_profile set to '1'


@pytest.mark.parametrize(
    'query, locale, expected_ids',
    [
        ('dut', 'en', ('afrikaans', 'dutch')),  # 'dut' is in aliases for Afrikaans and in main name for Dutch
        # the request is in Russian but IDs received are English:
        ('немец', 'ru', ('dutch', 'german', 'luxembourgian', 'swiss_german', 'yiddish')),
        # this query produces 7 doculects without 'has_feature_profile' restriction but only 3 with it:
        ('пар', 'ru', ('parachi', 'parthian', 'middle_persian'))
    ]

)
def test_get_doculects_by_substring(
        dummy_request, setup_models_for_views_testing,
        query, locale, expected_ids,
):

    dummy_request.locale_name = locale
    dummy_request.matchdict['query'] = query

    doculects = get_doculects_by_substring(dummy_request)

    assert len(doculects) == len(expected_ids)

    for doculect in doculects:
        for key in ('id', 'name', 'aliases', 'iso639p3Codes', 'glottocodes'):
            assert key in doculect.keys()

    for doculect_id in expected_ids:
        ids = [doculect['id'] for doculect in doculects]
        assert doculect_id in ids


@pytest.mark.parametrize(
    'locale, expected_first_doculect, expected_last_doculect',
    [
        (
            'ru',
            {'id': 'abaza', 'name': 'абазинский', 'latitude': 44.1556, 'longitude': 41.9368,
             'popupText': '<a href="/ru/doculect/abaza">абазинский</a>', 'url': '/ru/doculect/abaza'},
            {'id': 'yaoure', 'name': 'яурэ', 'latitude': 6.85, 'longitude': -5.3,
             'popupText': '<a href="/ru/doculect/yaoure">яурэ</a>', 'url': '/ru/doculect/yaoure'},
        ),
        (
            'en',
            {'id': 'abaza', 'name': 'Abaza', 'latitude': 44.1556, 'longitude': 41.9368,
             'popupText': '<a href="/en/doculect/abaza">Abaza</a>', 'url': '/en/doculect/abaza'},
            {'id': 'zefrei', 'name': 'Zefrei', 'latitude': 32.80592, 'longitude': 52.11667,
             'popupText': '<a href="/en/doculect/zefrei">Zefrei</a>', 'url': '/en/doculect/zefrei'},
        ),
    ]
)
def test_get_doculects_for_map(
        dummy_request, setup_models_for_views_testing, locale, expected_first_doculect, expected_last_doculect
):

    dummy_request.locale_name = locale
    groups = get_doculects_for_map(dummy_request)
    assert len(groups) == 1
    doculects = sorted(groups[0]['doculects'], key=lambda doculect: doculect['name'])

    assert len(doculects) == NUMBER_OF_TEST_DOCULECTS_WITH_FEATURE_PROFILES
    assert doculects[0] == expected_first_doculect
    assert doculects[-1] == expected_last_doculect


@pytest.mark.parametrize(
    'family_man_id, parent_is_none, expected_number_of_families',
    [   # subtracted numbers indicate families that have no doculects with profiles and must not be in data['families']
        (MATCHDICT_ID_FOR_ALL_FAMILIES, True, 13-2), ('isolate', False, 0), ('eskimo', False, 2-1), ('slav', False, 3)
    ]
)
def test_view_families_for_list(
        dummy_request, setup_models_for_views_testing, family_man_id, parent_is_none, expected_number_of_families
):
    dummy_request.locale_name = 'en'
    dummy_request.matchdict['family_man_id'] = family_man_id
    data = view_families_for_list(dummy_request)

    if parent_is_none:
        assert data['parent'] is None
    else:
        assert isinstance(data['parent'], Family)

    assert len(data['families']) == expected_number_of_families
    assert len(data['icon_for_family']) == expected_number_of_families + 1


@pytest.mark.parametrize(
    'family_man_id, expected_number_of_groups, expected_number_of_doculects',
    [
        # subtracted numbers indicate families that have no doculects
        (MATCHDICT_ID_FOR_ALL_FAMILIES, 13 - 2, NUMBER_OF_TEST_DOCULECTS_WITH_FEATURE_PROFILES),
        # addition indicates that a family that has subfamilies gets a group created for its immediate doculects
        # (even if this group ends up being empty)
        ('isolate', 1, 4), ('yupik', 1, 1), ('slav', 3 + 1, 16), ('avar_andi', 2 + 1, 14)
    ]
)
def test_view_families_for_map(
        dummy_request, setup_models_for_views_testing,
        family_man_id, expected_number_of_groups, expected_number_of_doculects
):
    dummy_request.locale_name = 'en'
    dummy_request.matchdict['family_man_id'] = family_man_id
    immediate_subfamilies = view_families_for_map(dummy_request)
    assert len(immediate_subfamilies) == expected_number_of_groups
    assert sum(len(group['doculects']) for group in immediate_subfamilies) == expected_number_of_doculects


def test_view_all_doculects_list(dummy_request, setup_models_for_views_testing):

    info = view_all_doculects_list(dummy_request)
    assert dummy_request.response.status_int == 200
    assert len(info['doculects']) == NUMBER_OF_TEST_DOCULECTS_WITH_FEATURE_PROFILES


def test_view_doculect_profile(dummy_request, setup_models_for_views_testing):
    dummy_request.matchdict['doculect_man_id'] = 'aragonese'

    info = view_doculect_profile(dummy_request)
    doculect = info['doculect']
    assert isinstance(doculect, Doculect)
    assert doculect.name_en == 'Aragonese'

    assert len(info['categories']) == 14


def test_view_doculect_profile_raises_not_found(dummy_request, setup_models_for_views_testing):
    dummy_request.matchdict['doculect_man_id'] = 'foo'

    with pytest.raises(pyramid.httpexceptions.HTTPNotFound):
        # I cannot check for presence of specific error message
        # because DummyRequest object has no 'exception' attribute.
        # Maybe app_request fixture can be used here instead.
        view_doculect_profile(dummy_request)


def test_families_get_parent_families_icons_not_found(dummy_request):
    dummy_request.matchdict['family_man_id'] = 'foo'
    with pytest.raises(pyramid.httpexceptions.HTTPNotFound):
        get_parent_families_icons(dummy_request)


def test_features_view_all_features_list_by_category(dummy_request, setup_models_for_views_testing):
    data = view_all_features_list_by_category(dummy_request)
    assert len(data['categories']) == 14
    for item in data['categories']:
        assert isinstance(item, FeatureCategory)


def test_features_get_feature_values_icons(dummy_request, setup_models_for_views_testing):
    dummy_request.matchdict['feature_man_id'] = 'H-6'
    feature, values, icon_for_value = get_feature_values_icons(dummy_request)

    assert feature.man_id == 'H-6'
    assert len(values) == 43 - 9  # there are 43 in total but 9 have no matching doculects
    assert len(icon_for_value) == len(values)
    assert len(set([i.svg_tag for i in icon_for_value.values()])) == len(values)  # make sure all icons are unique


def test_features_get_feature_values_icons_not_found(dummy_request, setup_models_for_views_testing):
    dummy_request.matchdict['feature_man_id'] = 'Z-99'

    with pytest.raises(pyramid.httpexceptions.HTTPNotFound):
        get_feature_values_icons(dummy_request)


def test_features_view_feature_list(dummy_request, setup_models_for_views_testing):
    dummy_request.matchdict['feature_man_id'] = 'H-6'
    data = view_feature_list_of_values(dummy_request)

    assert data['man_id'] == 'H-6'
    assert len(data['values']) == 43 - 9  # there are 43 in total but 9 have no matching doculects
    assert len(data['icon_for_value']) == len(data['values'])


def test_features_view_feature_map_of_values(dummy_request, setup_models_for_views_testing):
    dummy_request.locale_name = 'ru'
    dummy_request.matchdict['feature_man_id'] = 'H-6'
    groups = view_feature_map_of_values(dummy_request)
    # the number of groups must be equal to number of values that have at least one doculect
    assert len(groups) == 43 - 9
    assert sum(len(group['doculects']) for group in groups) == 104


def test_notfound_view(dummy_request):
    info = notfound_view(dummy_request)
    assert dummy_request.response.status_int == 404
    assert info == {}


# I'm not testing the building of params dict from URL as this is done by Pyramid.
# request.params is a NestedMultiDict, but I think passing a simple dictionary in test is OK.
@pytest.mark.parametrize(
    'params, expected_number_of_items, selected_doculects_to_check',
    [
        ({}, NUMBER_OF_TEST_DOCULECTS_WITH_FEATURE_PROFILES, []),
        ({'family': 'yupik'}, 1, ['asiatic_eskimo']),
        ({'family': 'yupik,aram'}, 8, ['asiatic_eskimo', 'classical_syriac', 'turoyo']),
        ({'family': 'yupik,aram'}, 8, ['asiatic_eskimo', 'classical_syriac', 'turoyo']),
        ({'family': 'south_chuk_kamch,chuk_kamch'}, 4, ['itelmen', 'kerek']),  # overlapping families
        # family + feature:
        ({'family': 'yupik,aram', 'A-11-1': 'A-11-1'}, 6, [
            'official_aramaic', 'jewish_palestinian_aramaic', 'classical_mandaic', 'neo_aramaic_of_maalula',
            'neo_mandaic', 'turoyo',
        ]),
        ({'family': 'yupik,aram', 'A-11-1': 'A-11-1,A-11-2'}, 6, [
            'official_aramaic', 'jewish_palestinian_aramaic', 'classical_mandaic', 'neo_aramaic_of_maalula',
            'neo_mandaic', 'turoyo',  # none of these languages has A-11-2
        ]),
        ({'family': 'yupik,aram', 'A-11-1': 'A-11-1,A-11-7'}, 7, [
            'official_aramaic', 'jewish_palestinian_aramaic', 'classical_mandaic', 'neo_aramaic_of_maalula',
            'neo_mandaic', 'turoyo', 'classical_syriac',
        ]),
        # family + 2 features:
        ({'family': 'yupik,aram', 'A-11-1': 'A-11-1,A-11-7', 'N-5': 'N-5-1'}, 5, [
            'official_aramaic', 'jewish_palestinian_aramaic', 'classical_mandaic', 'neo_aramaic_of_maalula',
            'turoyo',
        ]),
        ({'family': 'yupik,aram', 'A-11-1': 'A-11-1,A-11-7', 'N-5': 'N-5-1,N-5-3'}, 7, [
            'official_aramaic', 'jewish_palestinian_aramaic', 'classical_mandaic', 'neo_aramaic_of_maalula',
            'turoyo', 'neo_mandaic', 'classical_syriac',
        ]),
    ]
)
def test_query_wizard_get_matching_doculects(
        dummy_request, setup_models_for_views_testing,
        params, expected_number_of_items, selected_doculects_to_check
):
    dummy_request.params = params

    groups = get_matching_doculects(dummy_request)
    assert len(groups) == 1
    markers = groups[0]['doculects']
    assert len(markers) == expected_number_of_items

    for doculect_id in selected_doculects_to_check:
        assert doculect_id in [m['id'] for m in markers]
