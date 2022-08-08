from dataclasses import asdict, dataclass
from typing import Iterable, Optional

from langworld_db_pyramid.models import Doculect


@dataclass()
class DoculectDoculectMarkerGroupItem:
    """Provides individual data for specific doculect marker.
    Cannot function outside group of markers
    because data for icon generation is stored in the group.
    """
    id: str
    name: str
    latitude: float
    longitude: float
    popupText: str
    url: str


@dataclass()
class DoculectMarkerGroup:
    """Group of markers for a Leaflet map.
    All the markers within it share the same icon size, shape and color.
    """
    id: str
    name: str

    divIconHTML: str
    divIconSize: list

    doculects: list[DoculectDoculectMarkerGroupItem]


def generate_marker_group(
        group_id: str,
        group_name: str,
        div_icon_html: str,
        doculects: Iterable[Doculect],
        locale: str,
        additional_popup_text: Optional[str] = None,
) -> dict:
    """
    Generates a group of markers sharing the same icon style.

    Pop-up text for each marker defaults to doculect name with hyperlink to profile,
    additional pop-up text can be added via `additional_popup_text`.
    """
    # NOTE that this function returns a plain dictionary
    # and only uses classes for clarity within the module.
    return asdict(DoculectMarkerGroup(
        id=group_id,
        name=group_name,
        divIconHTML=div_icon_html,
        divIconSize=[40, 40],
        doculects=[
            _generate_marker_group_item(
                doculect=doculect,
                locale=locale,
                additional_popup_text=additional_popup_text,
            ) for doculect in doculects
        ]
    ))  # this will convert nested dataclasses to dicts as well.
    # I am not using NamedTuple because this trick with nested conversion does not work with it.


def _generate_marker_group_item(
        *,
        doculect: Doculect,
        locale: str,
        additional_popup_text: Optional[str] = None
) -> DoculectDoculectMarkerGroupItem:
    """Generates a dictionary with data for an individual marker within a group.

    Pop-up text defaults to doculect name with hyperlink to profile,
    additional pop-up text can be added via `additional_popup_text`.
    """
    name_attr = f'name_{locale}'

    longitude = float(doculect.longitude)
    if longitude < -170:
        longitude += 360

    doculect_name = f'{getattr(doculect, name_attr)} (†)' if doculect.is_extinct else getattr(doculect, name_attr)
    url = f'/{locale}/doculect/{doculect.man_id}'

    popup_text = f'<a href="{url}">{doculect_name}</a>'

    if additional_popup_text:
        popup_text = f'{popup_text}<br/>{additional_popup_text}'

    return DoculectDoculectMarkerGroupItem(
        id=doculect.man_id,
        name=doculect_name,
        latitude=float(doculect.latitude),
        longitude=longitude,
        popupText=popup_text,
        url=url,
    )
