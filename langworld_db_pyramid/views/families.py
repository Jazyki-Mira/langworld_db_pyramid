from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from .. import models

from langworld_db_pyramid.maputils.marker_icons import icon_for_object
from langworld_db_pyramid.maputils.markers import generate_marker_group

MATCHDICT_ID_FOR_ALL_FAMILIES = '_all'


def get_parent_families_icons(request):  # TODO test
    family_man_id = request.matchdict['family_man_id']

    if family_man_id == MATCHDICT_ID_FOR_ALL_FAMILIES:
        parent = None
        families = request.dbsession.scalars(select(models.Family).where(models.Family.parent == parent)).all()
    else:
        try:
            parent = request.dbsession.scalars(select(models.Family).where(models.Family.man_id == family_man_id)).one()
        except SQLAlchemyError:
            raise HTTPNotFound(f"Family with ID {family_man_id} does not exist")
        else:
            families = parent.children

    families_with_doculects_that_have_feature_profiles = [
        f for f in families if f.has_doculects_with_feature_profiles()
    ]

    # the point is to provide icons only for the top-level children
    icon_for_family = icon_for_object([parent] + families_with_doculects_that_have_feature_profiles)

    return parent, families_with_doculects_that_have_feature_profiles, icon_for_family


@view_config(route_name='families', renderer='langworld_db_pyramid:templates/families.jinja2')
@view_config(route_name='families_localized', renderer='langworld_db_pyramid:templates/families.jinja2')
def view_families_for_list(request):
    parent, families, icon_for_family = get_parent_families_icons(request)
    return {
        'parent': parent,
        'families': families,
        'icon_for_family': icon_for_family
    }


@view_config(route_name='doculects_for_map_family', renderer='json')
def view_families_for_map(request) -> list[dict]:
    parent, families, icon_for_family = get_parent_families_icons(request)
    locale = request.locale_name
    name_attr = "name_" + locale
    marker_groups = []

    if parent is not None:
        href = f"/{request.locale_name}/family/{parent.man_id}"

        marker_groups.append(generate_marker_group(
            group_id=parent.man_id,
            group_name=getattr(parent, name_attr),
            div_icon_html=icon_for_family[parent].svg_tag,
            href_for_heading_in_list=href,
            img_src=icon_for_family[parent].img_src,
            doculects=sorted(
                [d for d in parent.doculects if d.has_feature_profile], key=lambda d: getattr(d, name_attr)
            ),
            locale=locale,
            additional_popup_text=(
                f'(<a href="{href}">{getattr(parent, name_attr)}</a>)'
            )
        ))

    for family in families:
        href = f'/{request.locale_name}/family/{family.man_id}'
        marker_groups.append(
            generate_marker_group(
                group_id=family.man_id,
                group_name=getattr(family, name_attr),
                div_icon_html=icon_for_family[family].svg_tag,
                href_for_heading_in_list=href,
                img_src=icon_for_family[family].img_src,
                doculects=sorted(
                    list(family.iter_doculects_that_have_feature_profiles()),
                    key=lambda d: getattr(d, name_attr)
                ),
                locale=locale,
                additional_popup_text=(
                    f'(<a href="{href}">{getattr(family, name_attr)}</a>)'
                )
            )
        )

    return marker_groups
