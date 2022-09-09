from typing import Optional

from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from langworld_db_pyramid import models
from langworld_db_pyramid.dbutils.query_helpers import get_all, get_by_man_id
from langworld_db_pyramid.maputils.marker_icons import CLLDIcon, icon_for_object
from langworld_db_pyramid.maputils.markers import generate_marker_group

MATCHDICT_ID_FOR_ALL_FAMILIES = '_all'


def _get_family_immediate_subfamilies_and_icons(
        request) -> tuple[Optional[models.Family], list[models.Family], dict[models.Family, CLLDIcon]]:
    """Auxiliary function: returns the tuple consisting of
    the `Family` object from the database for the given family ID;
    objects for its immediate children; map/list icons for them.

    If '_all' is provided in `request.matchdict['family_man_id']`,
    top-level genealogy is returned: family is `None`,
    and immediate subfamilies are top-level families of the genealogy.
    """
    family_man_id = request.matchdict['family_man_id']

    if family_man_id == MATCHDICT_ID_FOR_ALL_FAMILIES:
        family = None
        immediate_subfamilies = get_all(request, select(models.Family).where(models.Family.parent == family))
    else:
        try:
            family = get_by_man_id(request=request, model=models.Family, man_id=family_man_id)
        except SQLAlchemyError:
            raise HTTPNotFound(f"Family with ID {family_man_id} does not exist")
        else:
            immediate_subfamilies = family.children

    # the point is to provide icons only for the requested family and its top-level children
    families_with_doculects_that_have_feature_profiles = [
        f for f in immediate_subfamilies if f.has_doculects_with_feature_profiles()
    ]
    icon_for_family = icon_for_object([family] + families_with_doculects_that_have_feature_profiles)

    return family, families_with_doculects_that_have_feature_profiles, icon_for_family


@view_config(route_name='families', renderer='langworld_db_pyramid:templates/families.jinja2')
@view_config(route_name='families_localized', renderer='langworld_db_pyramid:templates/families.jinja2')
def view_families_for_list(request):
    family, subfamilies, icon_for_family = _get_family_immediate_subfamilies_and_icons(request)
    return {'family': family, 'subfamilies': subfamilies, 'icon_for_family': icon_for_family}


@view_config(route_name='doculects_for_map_family', renderer='json')
def view_families_for_map(request) -> list[dict]:
    family, immediate_subfamilies, icon_for_family = _get_family_immediate_subfamilies_and_icons(request)
    locale = request.locale_name
    name_attr = "name_" + locale
    marker_groups = []

    if family is not None:
        href = f"/{request.locale_name}/family/{family.man_id}"

        marker_groups.append(
            generate_marker_group(group_id=family.man_id,
                                  group_name=getattr(family, name_attr),
                                  div_icon_html=icon_for_family[family].svg_tag,
                                  href_for_heading_in_list=href,
                                  img_src=icon_for_family[family].img_src,
                                  doculects=sorted([d for d in family.doculects if d.has_feature_profile],
                                                   key=lambda d: getattr(d, name_attr)),
                                  locale=locale,
                                  additional_popup_text=f'(<a href="{href}">{getattr(family, name_attr)}</a>)'))

    for subfamily in immediate_subfamilies:
        href = f'/{request.locale_name}/family/{subfamily.man_id}'
        marker_groups.append(
            generate_marker_group(group_id=subfamily.man_id,
                                  group_name=getattr(subfamily, name_attr),
                                  div_icon_html=icon_for_family[subfamily].svg_tag,
                                  href_for_heading_in_list=href,
                                  img_src=icon_for_family[subfamily].img_src,
                                  doculects=sorted(list(subfamily.iter_doculects_that_have_feature_profiles()),
                                                   key=lambda d: getattr(d, name_attr)),
                                  locale=locale,
                                  additional_popup_text=f'(<a href="{href}">{getattr(subfamily, name_attr)}</a>)'))

    return marker_groups
