from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from .. import models

from langworld_db_pyramid.maputils.generate_map_icons import icon_for_object
from langworld_db_pyramid.maputils.marker import generate_marker

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
def view_families_for_map(request):
    parent, families, icon_for_family = get_parent_families_icons(request)
    name_attr = "name_" + request.locale_name
    doculects = []

    if parent is not None:
        doculects = [
            generate_marker(
                request, doculect,
                div_icon_html=icon_for_family[parent].svg_tag,
                additional_popup_text=(
                    f'(<a href="/{request.locale_name}/family/{parent.man_id}">{getattr(parent, name_attr)}</a>)'
                )
            )
            for doculect in parent.doculects if doculect.has_feature_profile
        ]

    doculects += [
        generate_marker(
            request, doculect,
            div_icon_html=icon_for_family[family].svg_tag,
            additional_popup_text=(
                f'(<a href="/{request.locale_name}/family/{family.man_id}">{getattr(family, name_attr)}</a>)'
            )
        )
        for family in families
        for doculect in family.iter_doculects_that_have_feature_profiles()
    ]

    return doculects
