from clldutils import svg
from dataclasses import dataclass
from typing import Any, Iterator, Optional

COLORS = [
    '1f78b4', 'a6cee3', 'b2df8a', '33a02c', 'fb9a99', 'e31a1c', 'fdbf6f', 'ff7f00', 'cab2d6', '6a3d9a', 'ffff99',
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

    def __post_init__(self) -> None:
        self.svg_tag = self._generate_svg(self.shape_and_color)
        self.img_src = svg.data_url(self.svg_tag)
        self.img_tag = f'<img src="{self.img_src}"/>'

    def __eq__(self, other) -> bool:
        return self.svg_tag == other.svg_tag and self.img_tag == other.img_tag

    def __hash__(self) -> int:
        return hash((self.svg_tag, self.img_tag))

    def __repr__(self) -> str:
        return f'CLLDIcon (shape {self.shape_and_color[0]}, color #{self.shape_and_color[1:]})'

    @staticmethod
    def _generate_svg(spec: str, opacity: Optional[str] = None) -> str:
        """
        **This method is a copy** of function `icon()` in `clldutils.svg`
        with `paths` changed to produce smaller icons
        (since `icon()` does not allow to override the `paths`).

        Creates a SVG graphic according to a spec as used for map icons in `clld` apps.
        :param spec: Icon spec of the form "(s|d|c|f|t)rrggbb" where the first character defines a \
        shape (s=square, d=diamond, c=circle, f=upside-down triangle, t=triangle) and "rrggbb" \
        specifies a color as hex triple.
        :param opacity: Opacity
        :return: SVG XML
        """
        # different from clldutils.svg.icon() - smaller shapes:
        paths = {
            's': 'path d="M10 10 H30 V30 H10 V10"',
            'd': 'path d="M20 8 L32 20 L20 32 L8 20 L20 8"',
            'c': 'circle cx="20" cy="20" r="11"',
            'f': 'path d="M8 10 L32 10 L20 32 L8 10"',
            't': 'path d="M8 32 L32 32 L20 10 L8 32"',
        }
        # Changed calls to functions in clldutils.svg to dotted notation:
        elem = '<{0} style="{1}"/>'.format(
            # changed 'black' to dark grey hex (matter of taste)
            paths[spec[0]],
            svg.style(stroke='#585858', fill=svg.rgb_as_hex(spec[1:]), opacity=opacity))
        return svg.svg(elem, height=40, width=40)


def generate_map_icons() -> Iterator[CLLDIcon]:

    for shape in SHAPES:
        for color in COLORS:
            yield CLLDIcon(f'{shape}{color}')


def generate_fixed_number_of_map_icons(number: int) -> list[CLLDIcon]:
    """Returns list of icon HTMLs or one string with icon HTML if `number` is 1."""
    if number > len(SHAPES) * len(COLORS):
        raise ValueError(f'Cannot generate more than {len(COLORS) * len(SHAPES)} different markers')

    return [icon for _, icon in zip(range(number), generate_map_icons())]


def generate_one_icon() -> CLLDIcon:
    return generate_fixed_number_of_map_icons(1)[0]


def icon_for_object(objects: list) -> dict[Any, CLLDIcon]:
    """Gets a list of objects and returns a dictionary
    where each object is mapped to an icon.
    """
    if len(objects) > len(SHAPES) * len(COLORS):
        raise ValueError(f'Cannot generate more than {len(COLORS) * len(SHAPES)} different markers')

    return {obj: icon for obj, icon in zip(objects, generate_map_icons())}
