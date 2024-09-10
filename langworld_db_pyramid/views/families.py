from typing import Any, Optional, Union

from pyramid.request import Request
from pyramid.view import view_config
from sqlalchemy import select

from langworld_db_pyramid import models
from langworld_db_pyramid.dbutils.query_helpers import get_all
from langworld_db_pyramid.maputils.marker_icons import CLLDIcon, CLLDPie, icon_for_object
from langworld_db_pyramid.maputils.markers import generate_marker_group
from langworld_db_pyramid.views import (
    ID_TO_SHOW_ALL_DOCULECTS,
    get_doculect_from_params,
    localized_name_case_insensitive,
)


def _get_family_immediate_subfamilies_and_icons(
    request: Request,
) -> tuple[
    Optional[models.Family], list[models.Family], dict[models.Family, Union[CLLDIcon, CLLDPie]]
]:
    """Auxiliary function: returns the tuple consisting of
    the `Family` object from the database for the given family ID;
    objects for its immediate children; map/list icons for them.

    If '_all' is provided in `request.matchdict['family_man_id']`,
    top-level genealogy is returned: family is `None`,
    and immediate subfamilies are top-level families of the genealogy.
    """
    family_man_id = request.matchdict["family_man_id"]

    if family_man_id == ID_TO_SHOW_ALL_DOCULECTS:
        family = None
        immediate_subfamilies = get_all(
            request, select(models.Family).where(models.Family.parent == family)
        )
    else:
        family = models.Family.get_by_man_id(request=request, man_id=family_man_id)
        immediate_subfamilies = family.children

    # the point is to provide icons only for the requested family and its top-level children
    families_with_doculects_that_have_feature_profiles = [
        f for f in immediate_subfamilies if f.has_doculects_with_feature_profiles()
    ]
    icon_for_family = icon_for_object(
        [family] + families_with_doculects_that_have_feature_profiles
    )

    return family, families_with_doculects_that_have_feature_profiles, icon_for_family


@view_config(route_name="families", renderer="langworld_db_pyramid:templates/families.jinja2")
@view_config(
    route_name="families_localized", renderer="langworld_db_pyramid:templates/families.jinja2"
)
def view_families_for_list(request: Request) -> dict[str, Any]:
    family, subfamilies, icon_for_family = _get_family_immediate_subfamilies_and_icons(request)
    return {
        "family": family,
        "subfamilies": subfamilies,
        "icon_for_family": icon_for_family,
        "doculect_in_focus": get_doculect_from_params(request),
    }


@view_config(route_name="doculects_for_map_family", renderer="json")
def view_families_for_map(request: Request) -> list[dict[str, Any]]:
    family, immediate_subfamilies, icon_for_family = _get_family_immediate_subfamilies_and_icons(
        request
    )
    locale = request.locale_name
    name_attr = "name_" + locale
    marker_groups = []

    # We need to show a separate marker group for a family being requested only in two cases:
    # 1. This family is the terminal node on a family tree, e.g. has no children, OR
    # 2. This family has children but also has doculects "attached" immediately to it
    #    (this is likely due to a mistake in data, but we must be able to show doculects anyway)
    #
    # Check for truthiness of family is practically superfluous but is needed for mypy.
    if family and (family.doculects or not immediate_subfamilies):
        href = request.route_path("families_localized", locale=locale, family_man_id=family.man_id)
        marker_groups.append(
            generate_marker_group(
                request,
                group_id=family.man_id,
                group_name=getattr(family, name_attr),
                div_icon_html=icon_for_family[family].svg_tag,
                href_for_heading_in_list=href,
                img_src=icon_for_family[family].img_src,
                doculects=sorted(
                    [d for d in family.doculects if d.has_feature_profile],
                    key=localized_name_case_insensitive(locale),
                ),
                additional_popup_text=f'(<a href="{href}">{getattr(family, name_attr)}</a>)',
            )
        )

    for subfamily in immediate_subfamilies:
        href = request.route_path(
            "families_localized", locale=locale, family_man_id=subfamily.man_id
        )
        marker_groups.append(
            generate_marker_group(
                request,
                group_id=subfamily.man_id,
                group_name=getattr(subfamily, name_attr),
                div_icon_html=icon_for_family[subfamily].svg_tag,
                href_for_heading_in_list=href,
                img_src=icon_for_family[subfamily].img_src,
                doculects=sorted(
                    subfamily.iter_doculects_that_have_feature_profiles(),
                    key=localized_name_case_insensitive(locale),
                ),
                additional_popup_text=f'(<a href="{href}">{getattr(subfamily, name_attr)}</a>)',
            )
        )

    return marker_groups
