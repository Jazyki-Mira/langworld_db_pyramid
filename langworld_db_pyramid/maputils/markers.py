from collections.abc import Iterable
from dataclasses import asdict, dataclass
from typing import Any, Optional

from pyramid.request import Request

from langworld_db_pyramid.models import Doculect

LONGITUDE_TOO_FAR_WEST_THAT_NEEDS_CORRECTION_FOR_LEAFLET = -170


@dataclass
class DoculectMarkerGroupItem:
    """Provides individual data for specific doculect marker.
    Cannot function outside group of markers
    because data for icon generation is stored in the group.
    """

    id: str
    name: str
    latitude: float
    longitude: float
    popupText: str  # noqa: N815
    url: str


@dataclass()
class DoculectMarkerGroup:
    """Group of markers for a Leaflet map and interactive list.
    All the markers within it share the same icon size, shape and color.

    For the map: `divIconHTML` and `divIconSize`.
    For the list: `imgSrc` (icon next to heading), `href`
    (provide a non-empty string if a heading must be a link).
    """

    id: str
    name: str

    doculects: list[DoculectMarkerGroupItem]

    divIconHTML: str  # noqa: N815
    divIconSize: list[int]  # noqa: N815
    href: str
    imgSrc: str  # noqa: N815


def generate_marker_group(  # noqa: PLR0913
    request: Request,
    group_id: str,
    group_name: str,
    div_icon_html: str,
    doculects: Iterable[Doculect],
    img_src: str,
    additional_popup_text: Optional[str] = None,
    href_for_heading_in_list: Optional[str] = None,
) -> dict[str, Any]:
    """
    Generates a group of markers sharing the same icon style.

    Pop-up text for each marker defaults to doculect name with hyperlink to profile,
    additional pop-up text can be added via `additional_popup_text`.
    """
    # NOTE that this function returns a plain dictionary
    # and only uses classes for clarity within the module.
    return asdict(
        DoculectMarkerGroup(
            id=group_id,
            name=group_name,
            divIconHTML=div_icon_html,
            divIconSize=[40, 40],
            href=href_for_heading_in_list or "",
            imgSrc=img_src,
            doculects=[
                _generate_marker_group_item(
                    request,
                    doculect=doculect,
                    additional_popup_text=additional_popup_text,
                )
                for doculect in doculects
            ],
        )
    )  # this will convert nested dataclasses to dicts as well.
    # I am not using NamedTuple because this trick with nested conversion does not work with it.


def _generate_marker_group_item(
    request: Request, *, doculect: Doculect, additional_popup_text: Optional[str] = None
) -> DoculectMarkerGroupItem:
    """Generates a dictionary with data for an individual marker within a group.

    Pop-up text defaults to doculect name with hyperlink to profile,
    additional pop-up text can be added via `additional_popup_text`.
    """
    locale = request.locale_name
    name_attr = f"name_{locale}"

    longitude = float(doculect.longitude)
    if longitude < LONGITUDE_TOO_FAR_WEST_THAT_NEEDS_CORRECTION_FOR_LEAFLET:
        longitude += 360

    doculect_name = (
        f"{getattr(doculect, name_attr)} (†)"
        if doculect.is_extinct
        else getattr(doculect, name_attr)
    )
    url = request.route_path(
        "doculect_profile_localized", locale=locale, doculect_man_id=doculect.man_id
    )

    popup_text = f'<a href="{url}">{doculect_name}</a>'

    if additional_popup_text:
        popup_text = f"{popup_text}<br/>{additional_popup_text}"

    return DoculectMarkerGroupItem(
        id=doculect.man_id,
        name=doculect_name,
        latitude=float(doculect.latitude),
        longitude=longitude,
        popupText=popup_text,
        url=url,
    )
