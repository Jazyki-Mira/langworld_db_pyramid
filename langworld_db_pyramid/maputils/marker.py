from typing import NamedTuple, Optional

from langworld_db_pyramid.models import Doculect


class Marker(NamedTuple):
    """A class for a Leaflet map marker. """
    # these only depend on a doculect
    id: str
    name: str
    latitude: float
    longitude: float
    divIconSize: list
    url: str

    # these depend on the context of use
    divIconHTML: str
    popupText: str


def generate_marker(
        request, doculect: Doculect, *,
        div_icon_html: str, additional_popup_text: Optional[str] = None) -> dict:
    """Generates a dictionary with marker data.
    Most data is generated from doculect and request,
    but icon <svg> tag must be supplied.

    Pop-up text is defaults to doculect name with hyperlink to profile,
    additional pop-up text can be added via `additional_popup_text`.

    Returns dictionary, ready to be used in Javascript code.
    """
    # TODO test
    locale = request.locale_name
    name_attr = f'name_{locale}'

    longitude = float(doculect.longitude)
    if longitude < -170:
        longitude += 360

    doculect_name = f'{getattr(doculect, name_attr)} (†)' if doculect.is_extinct else getattr(doculect, name_attr)
    url = f'../doculect/{doculect.man_id}'

    popup_text = f'<a href="{url}">{doculect_name}</a>'

    if additional_popup_text:
        popup_text = f'{popup_text}<br/>{additional_popup_text}'

    return Marker(
        id=doculect.man_id,
        name=doculect_name,
        latitude=float(doculect.latitude),
        longitude=longitude,
        divIconHTML=div_icon_html,
        divIconSize=[40, 40],  # corresponds to size of icon in clldutils.svg
        popupText=popup_text,
        url=url,
    )._asdict()
