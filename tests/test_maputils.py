from typing import NamedTuple

import pytest

from langworld_db_pyramid.maputils.generate_map_icons import *


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
