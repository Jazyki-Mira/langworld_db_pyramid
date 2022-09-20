import pyramid.httpexceptions
import pytest
from sqlalchemy import select

from langworld_db_pyramid.dbutils.query_helpers import get_by_man_id, _get_one
from langworld_db_pyramid.models.doculect import Doculect
from langworld_db_pyramid.models.family import Family
from langworld_db_pyramid.models.feature_category import FeatureCategory
from langworld_db_pyramid.models.feature_value import FeatureValue
from langworld_db_pyramid.views.doculects_list import get_doculects_by_substring, view_all_doculects_list
from langworld_db_pyramid.views.doculects_map import get_doculects_for_map
from langworld_db_pyramid.views.doculect_profile import view_doculect_profile
from langworld_db_pyramid.views.families import (_get_family_immediate_subfamilies_and_icons,
                                                 MATCHDICT_ID_FOR_ALL_FAMILIES, view_families_for_list,
                                                 view_families_for_map)
from langworld_db_pyramid.views.features import (get_feature_values_icons, view_all_features_list_by_category,
                                                 view_feature_list_of_values, view_feature_map_of_values)
from langworld_db_pyramid.views.mapbox_token import get_mapbox_token
from langworld_db_pyramid.views.notfound import notfound_view
from langworld_db_pyramid.views.query_wizard import get_matching_doculects

NUMBER_OF_TEST_DOCULECTS_WITH_FEATURE_PROFILES = 338  # only those (out of 429) that have has_feature_profile set to '1'
NUMBER_OF_TEST_TOP_LEVEL_FAMILIES_WITH_FEATURE_PROFILES = 11  # only 11 out of 13 have doculects with feature profiles


@pytest.mark.parametrize(
    'query, locale, expected_ids',
    [
        ('dut', 'en', ('afrikaans', 'dutch')),  # 'dut' is in aliases for Afrikaans and in main name for Dutch
        # the request is in Russian but IDs received are English. Sort results by Russian name:
        ('немец', 'ru', ('yiddish', 'luxembourgian', 'german', 'dutch', 'swiss_german')),
        # this query produces 7 doculects without 'has_feature_profile' restriction but only 3 with it:
        ('пар', 'ru', ('parachi', 'parthian', 'middle_persian')),
        # glottocode
        ('nucl1', 'ru', ('georgian', 'kannada', 'neo_mandaic', 'pashto', 'turkish', 'japanese')),
        # matches both ISO code and name (balochi), only part of name (karachay_balkar); balochi has 3 glottocodes
        ('bal', 'en', ('balochi', 'karachay_balkar')),
        # chagatai has turki as alias; turki has neither ISO code nor glottocode, which can affect search
        ('тюрки', 'ru', ('turki', 'chagatai')),
        # biyabuneki has glottocode but no ISO code
        ('бия', 'ru', ('biyabuneki', )),  # searching by name
        ('biya', 'ru', ('biyabuneki', )),  # searching by glottocode
        ('xcr', 'ru', ('carian', ))  # searching by ISO code
    ])
def test_get_doculects_by_substring(
    dummy_request,
    setup_models_once_for_test_module,
    query,
    locale,
    expected_ids,
):

    dummy_request.locale_name = locale
    dummy_request.matchdict['query'] = query

    doculects = get_doculects_by_substring(dummy_request)

    assert len(doculects) == len(expected_ids)

    for doculect in doculects:
        for key in ('id', 'name', 'aliases', 'iso639p3Codes', 'glottocodes'):
            assert key in doculect.keys()

    for i, doculect_id in enumerate(expected_ids):
        ids = [doculect['id'] for doculect in doculects]
        assert doculect_id == ids[i]  # check not just membership, but also sorting


def test_get_doculects_by_substring_returns_empty_list_if_nothing_found(dummy_request,
                                                                        setup_models_once_for_test_module):
    dummy_request.locale_name = 'en'
    dummy_request.matchdict['query'] = 'foo'

    doculects = get_doculects_by_substring(dummy_request)

    assert isinstance(doculects, list)
    assert len(doculects) == 0


@pytest.mark.parametrize('locale, expected_first_doculect, expected_last_doculect', [
    (
        'ru',
        {
            'id': 'abaza',
            'name': 'абазинский',
            'latitude': 44.1556,
            'longitude': 41.9368,
            'popupText': '<a href="/ru/doculect/abaza">абазинский</a>',
            'url': '/ru/doculect/abaza'
        },
        {
            'id': 'yaoure',
            'name': 'яурэ',
            'latitude': 6.85,
            'longitude': -5.3,
            'popupText': '<a href="/ru/doculect/yaoure">яурэ</a>',
            'url': '/ru/doculect/yaoure'
        },
    ),
    (
        'en',
        {
            'id': 'abaza',
            'name': 'Abaza',
            'latitude': 44.1556,
            'longitude': 41.9368,
            'popupText': '<a href="/en/doculect/abaza">Abaza</a>',
            'url': '/en/doculect/abaza'
        },
        {
            'id': 'zefrei',
            'name': 'Zefrei',
            'latitude': 32.80592,
            'longitude': 52.11667,
            'popupText': '<a href="/en/doculect/zefrei">Zefrei</a>',
            'url': '/en/doculect/zefrei'
        },
    ),
])
def test_get_doculects_for_map(dummy_request, dummy_config, setup_models_once_for_test_module,
                               locale, expected_first_doculect, expected_last_doculect):

    dummy_request.locale_name = locale
    groups = get_doculects_for_map(dummy_request)
    assert len(groups) == 1
    doculects = sorted(groups[0]['doculects'], key=lambda doculect: doculect['name'])

    assert len(doculects) == NUMBER_OF_TEST_DOCULECTS_WITH_FEATURE_PROFILES
    assert doculects[0] == expected_first_doculect
    assert doculects[-1] == expected_last_doculect


@pytest.mark.parametrize('family_man_id, expected_number_of_subfamilies, expected_number_of_icon_groups', [
    ('_all', NUMBER_OF_TEST_TOP_LEVEL_FAMILIES_WITH_FEATURE_PROFILES,
     NUMBER_OF_TEST_TOP_LEVEL_FAMILIES_WITH_FEATURE_PROFILES),
    ('turk', 8, 9),
    ('isolate', 0, 1),
    ('yupik', 0, 1),
    ('slav', 3, 4),
    ('avar_andi', 2, 3),
])
def test_families__get_family_immediate_subfamilies_and_icons(dummy_request, setup_models_once_for_test_module,
                                                              family_man_id, expected_number_of_subfamilies,
                                                              expected_number_of_icon_groups):
    dummy_request.matchdict['family_man_id'] = family_man_id
    parent, families, dict_with_icons = _get_family_immediate_subfamilies_and_icons(dummy_request)
    if family_man_id == MATCHDICT_ID_FOR_ALL_FAMILIES:
        assert parent is None
    else:
        assert parent.man_id == family_man_id
    assert len(families) == expected_number_of_subfamilies


def test_families__get_family_immediate_subfamilies_and_icons_not_found(dummy_request):
    dummy_request.matchdict['family_man_id'] = 'foo'
    with pytest.raises(pyramid.httpexceptions.HTTPNotFound):
        _get_family_immediate_subfamilies_and_icons(dummy_request)


@pytest.mark.parametrize(
    'family_man_id, parent_is_none, expected_number_of_families',
    [  # subtracted numbers indicate families that have no doculects with profiles and must not be in data['families']
        (MATCHDICT_ID_FOR_ALL_FAMILIES, True, 13 - 2), ('isolate', False, 0), ('eskimo', False, 2 - 1),
        ('slav', False, 3)
    ])
def test_view_families_for_list(dummy_request, setup_models_once_for_test_module, family_man_id, parent_is_none,
                                expected_number_of_families):
    dummy_request.locale_name = 'en'
    dummy_request.matchdict['family_man_id'] = family_man_id
    data = view_families_for_list(dummy_request)

    if parent_is_none:
        assert data['family'] is None
    else:
        assert isinstance(data['family'], Family)

    assert len(data['subfamilies']) == expected_number_of_families
    assert len(data['icon_for_family']) == expected_number_of_families + 1


def test_mapbox_token_get_mapbox_token(app_request):  # dummy_request won't have access to request.registry.settings
    token = get_mapbox_token(app_request)
    assert token.startswith('sk.')


@pytest.mark.parametrize(
    'family_man_id, expected_number_of_groups, expected_number_of_doculects',
    [
        (MATCHDICT_ID_FOR_ALL_FAMILIES, NUMBER_OF_TEST_TOP_LEVEL_FAMILIES_WITH_FEATURE_PROFILES,
         NUMBER_OF_TEST_DOCULECTS_WITH_FEATURE_PROFILES),
        # addition indicates that a family that has subfamilies gets a group created for its immediate doculects
        # (even if this group ends up being empty)
        ('isolate', 1, 4),
        ('yupik', 1, 1),
        ('slav', 3 + 1, 16),
        ('avar_andi', 2 + 1, 14)
    ])
def test_view_families_for_map(dummy_request, dummy_config, setup_models_once_for_test_module, family_man_id,
                               expected_number_of_groups, expected_number_of_doculects):
    dummy_request.locale_name = 'en'
    dummy_request.matchdict['family_man_id'] = family_man_id
    immediate_subfamilies = view_families_for_map(dummy_request)
    assert len(immediate_subfamilies) == expected_number_of_groups
    assert sum(len(group['doculects']) for group in immediate_subfamilies) == expected_number_of_doculects


def test_view_all_doculects_list(dummy_request, setup_models_once_for_test_module):

    data = view_all_doculects_list(dummy_request)
    assert dummy_request.response.status_int == 200
    assert len(data['doculects']) == NUMBER_OF_TEST_DOCULECTS_WITH_FEATURE_PROFILES
    assert len(data['volumes']) == 19


def test_view_doculect_profile(dummy_request, setup_models_once_for_test_module):
    dummy_request.matchdict['doculect_man_id'] = 'aragonese'

    data = view_doculect_profile(dummy_request)
    doculect = data['doculect']
    assert isinstance(doculect, Doculect)
    assert doculect.name_en == 'Aragonese'

    assert len(data['categories']) == 14

    comment_for_value = data['comment_for_feature_value']
    assert len(comment_for_value) == 21

    for man_id in ('K-1-3', 'K-2-3'):
        value = get_by_man_id(request=dummy_request, model=FeatureValue, man_id=man_id)
        assert value in comment_for_value


def test_view_doculect_profile_raises_not_found(dummy_request, setup_models_once_for_test_module):
    dummy_request.matchdict['doculect_man_id'] = 'foo'

    with pytest.raises(pyramid.httpexceptions.HTTPNotFound):
        # I cannot check for presence of specific error message
        # because DummyRequest object has no 'exception' attribute.
        # Maybe app_request fixture can be used here instead.
        view_doculect_profile(dummy_request)


def test_features_view_all_features_list_by_category(dummy_request, setup_models_once_for_test_module):
    data = view_all_features_list_by_category(dummy_request)
    assert len(data['categories']) == 14
    for item in data['categories']:
        assert isinstance(item, FeatureCategory)


def test_features_get_feature_values_icons(dummy_request, setup_models_once_for_test_module):
    dummy_request.matchdict['feature_man_id'] = 'H-6'
    feature, values, icon_for_value = get_feature_values_icons(dummy_request)

    assert feature.man_id == 'H-6'
    assert len(values) == 43 - 9  # there are 43 in total but 9 have no matching doculects
    assert len(icon_for_value) == len(values)
    assert len(set([i.svg_tag for i in icon_for_value.values()])) == len(values)  # make sure all icons are unique


def test_features_get_feature_values_icons_not_found(dummy_request, setup_models_once_for_test_module):
    dummy_request.matchdict['feature_man_id'] = 'Z-99'

    with pytest.raises(pyramid.httpexceptions.HTTPNotFound):
        get_feature_values_icons(dummy_request)


def test_features_view_feature_list_of_values(dummy_request, setup_models_once_for_test_module):
    dummy_request.matchdict['feature_man_id'] = 'H-6'
    data = view_feature_list_of_values(dummy_request)

    assert data['man_id'] == 'H-6'


def test_features_view_feature_map_of_values(dummy_request, dummy_config, setup_models_once_for_test_module):
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
        ({
            'family': 'yupik'
        }, 1, ['asiatic_eskimo']),
        ({
            'family': 'yupik,aram'
        }, 8, ['asiatic_eskimo', 'classical_syriac', 'turoyo']),
        ({
            'family': 'yupik,aram'
        }, 8, ['asiatic_eskimo', 'classical_syriac', 'turoyo']),
        ({
            'family': 'south_chuk_kamch,chuk_kamch'
        }, 4, ['itelmen', 'kerek']),  # overlapping families
        # family + feature:
        ({
            'family': 'yupik,aram',
            'A-11-1': 'A-11-1'
        }, 6, [
            'official_aramaic',
            'jewish_palestinian_aramaic',
            'classical_mandaic',
            'neo_aramaic_of_maalula',
            'neo_mandaic',
            'turoyo',
        ]),
        (
            {
                'family': 'yupik,aram',
                'A-11-1': 'A-11-1,A-11-2'
            },
            6,
            [
                'official_aramaic',
                'jewish_palestinian_aramaic',
                'classical_mandaic',
                'neo_aramaic_of_maalula',
                'neo_mandaic',
                'turoyo',  # none of these languages has A-11-2
            ]),
        ({
            'family': 'yupik,aram',
            'A-11-1': 'A-11-1,A-11-7'
        }, 7, [
            'official_aramaic',
            'jewish_palestinian_aramaic',
            'classical_mandaic',
            'neo_aramaic_of_maalula',
            'neo_mandaic',
            'turoyo',
            'classical_syriac',
        ]),
        # family + 2 features:
        ({
            'family': 'yupik,aram',
            'A-11-1': 'A-11-1,A-11-7',
            'N-5': 'N-5-1'
        }, 5, [
            'official_aramaic',
            'jewish_palestinian_aramaic',
            'classical_mandaic',
            'neo_aramaic_of_maalula',
            'turoyo',
        ]),
        ({
            'family': 'yupik,aram',
            'A-11-1': 'A-11-1,A-11-7',
            'N-5': 'N-5-1,N-5-3'
        }, 7, [
            'official_aramaic',
            'jewish_palestinian_aramaic',
            'classical_mandaic',
            'neo_aramaic_of_maalula',
            'turoyo',
            'neo_mandaic',
            'classical_syriac',
        ]),
    ])
def test_query_wizard_get_matching_doculects(dummy_request, dummy_config, setup_models_once_for_test_module, params,
                                             expected_number_of_items, selected_doculects_to_check):
    dummy_request.params = params
    print(dummy_request.route_path('doculect_profile_localized', locale='en', doculect_man_id='french'))
    groups = get_matching_doculects(dummy_request)
    assert len(groups) == 1
    markers = groups[0]['doculects']
    assert len(markers) == expected_number_of_items

    for doculect_id in selected_doculects_to_check:
        assert doculect_id in [m['id'] for m in markers]
