from clldutils import svg
from dataclasses import dataclass
from typing import Iterator, Union

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
    """A convenience class that takes string in style of clldutils.svg
    and produces object with two attributes needed for displaying an icon
    either inline (use value of `.img_src` instead of ... in <img src="..." />)
    or on a map (use `.svg_html`, for example, in `.html` attribute of `L.divIcon`)
    """
    shape_and_color: str

    def __post_init__(self):
        self.svg_tag = svg.icon(self.shape_and_color)
        self.img_src = svg.data_url(self.svg_tag)


def generate_map_icons() -> Iterator[CLLDIcon]:

    for shape in SHAPES:
        for color in COLORS:
            yield CLLDIcon(f'{shape}{color}')
            # TODO test if I decide to use this

    raise ValueError(f'Cannot generate more than {len(COLORS) * len(SHAPES)} different markers')


def generate_fixed_number_of_map_icons(number) -> Union[CLLDIcon, list[CLLDIcon]]:
    """Returns list of icon HTMLs or one string with icon HTML if `number` is 1."""
    if number > len(SHAPES) * len(COLORS):
        raise ValueError(f'Cannot generate more than {len(COLORS) * len(SHAPES)} different markers')

    icons = [icon for _, icon in zip(range(number), generate_map_icons())]
    return icons[0] if number == 1 else icons
