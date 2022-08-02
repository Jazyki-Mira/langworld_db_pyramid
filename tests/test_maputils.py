from typing import NamedTuple

import pytest
from sqlalchemy import select

from langworld_db_pyramid.maputils.marker_icons import *
from langworld_db_pyramid.maputils.markers import _generate_marker_group_item, generate_marker_group
from langworld_db_pyramid.models import Doculect


class DummyObject(NamedTuple):
    x: int
    y: int


def test_clld_icon__post_init__():
    icon = CLLDIcon('c000000')
    assert '<svg' in icon.svg_tag and '000000' in icon.svg_tag
    assert icon.img_src.startswith('data:image/svg+xml')


def test_clld_icon_dunder_methods():
    icon1 = CLLDIcon('c000000')
    icon2 = CLLDIcon('cffffff')
    assert len({icon1, icon2}) == 2

    icon3 = CLLDIcon('d000000')
    icon4 = CLLDIcon('c000000')
    assert icon4 == icon1
    assert icon3 != icon1

    assert str(icon1) == 'CLLDIcon (shape c, color #000000)'


def test_generate_map_icons():
    icons = [icon for icon, _ in zip(generate_map_icons(), range(60))]
    assert len(icons) == 60
    assert len(set(icons)) == len(icons)


def test_generate_fixed_number_of_map_icons():
    icons = generate_fixed_number_of_map_icons(60)
    assert len(icons) == 60
    assert len(set(icons)) == len(icons)


def test_generate_fixed_number_of_map_icons_fails_for_more_than_max_number():
    with pytest.raises(ValueError) as e:
        generate_fixed_number_of_map_icons(61)
    assert 'Cannot generate more than' in str(e)


def test__generate_marker_group_item(setup_models_for_views_testing, dbsession):
    doculect = dbsession.scalars(select(Doculect).where(Doculect.man_id == 'asiatic_eskimo')).one()
    data = _generate_marker_group_item(
        doculect=doculect,
        locale='en',
        additional_popup_text='foo'
    )
    assert data['name'] == doculect.name_en
    assert data['latitude'] == float(doculect.latitude)
    assert data['longitude'] == float(doculect.longitude) + 360  # testing doculect with longitude -173.128
    assert data['popupText'] == f'<a href="/en/doculect/{doculect.man_id}">{doculect.name_en}</a><br/>foo'
    assert data['url'] == f'/en/doculect/{doculect.man_id}'


def test_generate_marker_group(setup_models_for_views_testing, dbsession):
    eskimo = dbsession.scalars(select(Doculect).where(Doculect.man_id == 'asiatic_eskimo')).one()
    old_french = dbsession.scalars(select(Doculect).where(Doculect.man_id == 'old_french')).one()

    group = generate_marker_group(
        group_id='test_id',
        group_name='test_name',
        div_icon_html='will be received elsewhere',
        doculects=[eskimo, old_french],
        locale='en',
        additional_popup_text='foo',
    )
    assert group['id'] == 'test_id'
    assert group['name'] == 'test_name'
    assert len(group['markers']) == 2

    eskimo_data = group['markers'][0]
    assert eskimo_data['name'] == eskimo.name_en
    assert eskimo_data['latitude'] == float(eskimo.latitude)
    assert eskimo_data['longitude'] == float(eskimo.longitude) + 360  # testing doculect with longitude -173.128
    assert eskimo_data['popupText'] == f'<a href="/en/doculect/{eskimo.man_id}">{eskimo.name_en}</a><br/>foo'
    assert eskimo_data['url'] == f'/en/doculect/{eskimo.man_id}'

    old_french_data = group['markers'][1]
    assert old_french_data['name'] == old_french.name_en + ' (†)'
    assert old_french_data['latitude'] == float(old_french.latitude)
    assert old_french_data['longitude'] == float(old_french.longitude)
    assert old_french_data['popupText'] == (
        f'<a href="/en/doculect/{old_french.man_id}">{old_french.name_en} (†)</a><br/>foo'
    )
    assert old_french_data['url'] == f'/en/doculect/{old_french.man_id}'


def test_icon_for_object():
    dummy_objects = [DummyObject(i, i) for i in range(60)]
    icon_for_dummy_object = icon_for_object(dummy_objects)

    assert len(icon_for_dummy_object) == 60
    for i, key in enumerate(icon_for_dummy_object):
        assert key == dummy_objects[i]

    # checking uniqueness of icons
    assert len(set(icon_for_dummy_object.values())) == 60


def test_icon_for_object_fails_for_more_than_max_number():
    with pytest.raises(ValueError) as e:
        _ = icon_for_object([DummyObject(i, i) for i in range(61)])
    assert 'Cannot generate more than' in str(e)
