from clldutils import svg
from dataclasses import dataclass
from typing import Any, Iterator, Union

COLORS = [
    '1f78b4',
    'a6cee3',
    'b2df8a',
    '33a02c',
    'fb9a99',
    'e31a1c',
    'fdbf6f',
    'ff7f00',
    'cab2d6',
    '6a3d9a',
    'ffff99',
    'b15928'
]

SHAPES = ('c', 's', 't', 'd', 'f')


@dataclass
class CLLDIcon:
    """A convenience class that takes string in style of `clldutils.svg`
    and produces object with two attributes needed for displaying an icon
    either inline (value of `.img_tag` gives `<img src="<svg_code_of_the_icon>" />`
    for Python-rendered content; value of `.img_src` gives contents of <img src=".../">
    for use in Javascript when generating an <img> element)
    or on a map (use `.svg_tag`, for example, in `.html` attribute of `L.divIcon`).

    Note that use of `.img_tag` in Jinja templates will require `|safe` filter,
    otherwise some characters will be escaped.
    """
    shape_and_color: str

    def __post_init__(self):
        self.svg_tag = svg.icon(self.shape_and_color)
        self.img_src = svg.data_url(self.svg_tag)
        self.img_tag = f'<img src="{self.img_src}"/>'

    def __eq__(self, other):
        if self.shape_and_color == other.shape_and_color:
            return True
        return False

    def __hash__(self):
        return hash((self.svg_tag, self.img_tag))

    def __repr__(self):
        return f'CLLDIcon (shape {self.shape_and_color[0]}, color #{self.shape_and_color[1:]})'


def generate_map_icons() -> Iterator[CLLDIcon]:

    for shape in SHAPES:
        for color in COLORS:
            yield CLLDIcon(f'{shape}{color}')


def generate_fixed_number_of_map_icons(number) -> Union[CLLDIcon, list[CLLDIcon]]:
    """Returns list of icon HTMLs or one string with icon HTML if `number` is 1."""
    if number > len(SHAPES) * len(COLORS):
        raise ValueError(f'Cannot generate more than {len(COLORS) * len(SHAPES)} different markers')

    icons = [icon for _, icon in zip(range(number), generate_map_icons())]
    return icons[0] if number == 1 else icons


def icon_for_object(objects: list) -> dict[Any, CLLDIcon]:
    """Gets a list of objects and returns a dictionary
    where each object is mapped to an icon.
    """
    if len(objects) > len(SHAPES) * len(COLORS):
        raise ValueError(f'Cannot generate more than {len(COLORS) * len(SHAPES)} different markers')

    return {obj: icon for obj, icon in zip(objects, generate_map_icons())}
