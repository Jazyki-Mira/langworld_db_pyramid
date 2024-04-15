import math
from collections.abc import Iterator
from typing import Any, Optional, Union
from xml.sax.saxutils import escape

from clldutils import svg
from clldutils.color import qualitative_colors, rgb_as_hex

COLORS = [
    "a6cee3",
    "1f78b4",
    "b2df8a",
    "33a02c",
    "fb9a99",
    "e31a1c",
    "fdbf6f",
    "ff7f00",
    "cab2d6",
    "6a3d9a",
    "ffff99",
    "b15928",
]
SHAPES = ("c", "s", "t", "d", "f")

COLOR_FOR_EMPTY_VALUE = "faf9f6"  # "off-white"
OPACITY_FOR_EMPTY_VALUE = "45%"


class AbstractCLLDIcon:
    def __eq__(self, other: object) -> bool:
        return self.svg_tag == getattr(other, "svg_tag", None) and self.img_tag == getattr(
            other, "img_tag", None
        )

    def __hash__(self) -> int:
        return hash((self.svg_tag, self.img_tag))

    @property
    def img_src(self) -> str:
        return svg.data_url(self.svg_tag)

    @property
    def img_tag(self) -> str:
        return f'<img src="{self.img_src}"/>'

    @property
    def svg_tag(self) -> str:
        raise NotImplementedError


class CLLDIcon(AbstractCLLDIcon):
    """A convenience class that takes string in style of `clldutils.svg`
    and produces object with two attributes needed for displaying an icon
    either inline (value of `.img_tag` gives `<img src="<svg_code_of_the_icon>" />`
    for Python-rendered content; value of `.img_src` gives contents of <img src=".../">
    for use in Javascript when generating an <img> element)
    or on a map (use `.svg_tag`, for example, in `.html` attribute of `L.divIcon`).

    Note that use of `.img_tag` in Jinja templates will require `|safe` filter,
    otherwise some characters will be escaped.
    """

    def __init__(self, shape_and_color: str, opacity: Union[str, None] = None) -> None:
        super().__init__()
        self.shape_and_color = shape_and_color
        self.shape, self.color = self.shape_and_color[0], self.shape_and_color[1:]
        self.opacity = opacity

    def __repr__(self) -> str:
        return f"CLLDIcon (shape {self.shape}, color #{self.color})"

    @property
    def svg_tag(self) -> str:
        return self._generate_svg()

    def _generate_svg(self) -> str:
        """
        Creates an SVG graphic according to a spec as used for map icons in `clld` apps.

        **This method is a copy** of function `icon()` in `clldutils.svg`
        with `paths` changed to produce smaller icons
        (since `icon()` does not allow to override the `paths`).

        :return: SVG XML
        """
        # different from clldutils.svg.icon() - smaller shapes:
        paths = {
            "s": 'path d="M10 10 H30 V30 H10 V10"',
            "d": 'path d="M20 8 L32 20 L20 32 L8 20 L20 8"',
            "c": 'circle cx="20" cy="20" r="11"',
            "f": 'path d="M8 10 L32 10 L20 32 L8 10"',
            "t": 'path d="M8 32 L32 32 L20 10 L8 32"',
        }
        # Changed calls to functions in clldutils.svg to dotted notation:
        elem = '<{} style="{}"/>'.format(
            # changed 'black' to dark grey hex (matter of taste)
            paths[self.shape_and_color[0]],
            svg.style(
                stroke="#585858",
                fill=svg.rgb_as_hex(self.shape_and_color[1:]),
                opacity=self.opacity,
            ),
        )
        return svg.svg(elem, height=40, width=40)


class CLLDPie(AbstractCLLDIcon):
    """A class for a CLLD pie chart"""

    def __init__(self, colors: list[str]) -> None:
        super().__init__()
        self.colors: list[str] = colors

    def __repr__(self) -> str:
        return f"CLLD pie (colors {', '.join(self.colors)})"

    @property
    def svg_tag(self) -> str:
        return self.pie(
            # generate a list of equal numbers that add up to 100
            data=[100 / len(self.colors)] * len(self.colors),
            colors=self.colors,
            width=24,
        )

    @staticmethod
    def pie(
        data: list[Union[float, int]],
        colors: Optional[list[str]] = None,
        titles: Optional[list[str]] = None,
        width: int = 34,
        stroke_circle: bool = False,
    ) -> str:
        """
        An SVG pie chart.

        **Copied** from `clldutils.svg` with **changed cx, cy and width**
        to match coordinates of circle marker.
        (Also changed some dotted syntax in imported modules).
        """
        colors = qualitative_colors(len(data)) if colors is None else colors
        assert len(data) == len(colors)
        zipped = [(d, c) for d, c in zip(data, colors) if d != 0]
        data, colors = [z[0] for z in zipped], [z[1] for z in zipped]
        # (width + width / 1.5) instead of just width ensures a match with circle marker's position
        cx = cy = round((width + width / 1.5) / 2, 1)
        radius = round((width - 2) / 2, 1)
        current_angle_rad = 0
        svg_content = []
        total = sum(data)
        titles = titles or [None] * len(data)  # type: ignore
        stroke_circle = "black" if stroke_circle is True else stroke_circle or "none"  # type: ignore  # noqa

        def endpoint(angle_rad: float) -> tuple[float, float]:
            """
            Calculate position of point on circle given an angle, a radius, and the location
            of the center of the circle. Zero line points west.
            """
            return (
                round(cx - (radius * math.cos(angle_rad)), 1),
                round(cy - (radius * math.sin(angle_rad)), 1),
            )

        if len(data) == 1:
            svg_content.append(
                f'<circle cx="{cx}" cy="{cy}" r="{radius}" style="stroke:{stroke_circle}; fill:{rgb_as_hex(colors[0])};">'
            )
            if titles[0]:
                svg_content.append(f"<title>{escape(titles[0])}</title>")
            svg_content.append("</circle>")
            return svg.svg("".join(svg_content), height=width, width=width)

        for angle_deg, color, title in zip([360.0 / total * d for d in data], colors, titles):
            radius1 = "M{},{} L{},{}".format(cx, cy, *endpoint(current_angle_rad))
            current_angle_rad += math.radians(angle_deg)  # type: ignore
            arc = "A{},{} 0 {},1 {} {}".format(
                radius, radius, 1 if angle_deg > 180 else 0, *endpoint(current_angle_rad)  # noqa
            )
            radius2 = f"L{cx},{cy}"
            svg_content.append(
                f'<path d="{radius1} {arc} {radius2}" style="{svg.style(fill=rgb_as_hex(color))}" transform="rotate(90 {cx} {cy})">'
            )
            if title:
                svg_content.append(f"<title>{escape(title)}</title>")
            svg_content.append("</path>")

        if stroke_circle != "none":  # type: ignore
            svg_content.append(
                f'<circle cx="{cx}" cy="{cy}" r="{radius}" style="stroke:{stroke_circle}; '
                f'fill:none;"/>'
            )

        width = int(width * 1.5)  # to show full pie while still matching circle marker's position
        return svg.svg("".join(svg_content), height=width, width=width)


def generate_map_icons() -> Iterator[CLLDIcon]:
    yield from (CLLDIcon(f"{shape}{color}") for shape in SHAPES for color in COLORS)


def generate_fixed_number_of_map_icons(number: int) -> list[CLLDIcon]:
    """Returns list of icon HTMLs or one string with icon HTML if `number` is 1."""
    if number > len(SHAPES) * len(COLORS):
        raise ValueError(
            f"Cannot generate more than {len(COLORS) * len(SHAPES)} different markers"
        )

    return [icon for _, icon in zip(range(number), generate_map_icons())]


def generate_one_icon() -> CLLDIcon:
    return generate_fixed_number_of_map_icons(1)[0]


def icon_for_object(objects: list[object]) -> dict[Any, Union[CLLDIcon, CLLDPie]]:
    """Gets a list of objects and returns a dictionary where each object is mapped to an icon."""
    if len(objects) > len(SHAPES) * len(COLORS):
        raise ValueError(
            f"Cannot generate more than {len(COLORS) * len(SHAPES)} different markers"
        )

    return dict(zip(objects, generate_map_icons()))
