from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from .. import models

from langworld_db_pyramid.maputils.generate_map_icons import icon_for_object

MATCHDICT_ID_FOR_ALL_FAMILIES = '_all'


@view_config(route_name='families', renderer='langworld_db_pyramid:templates/families.jinja2')
@view_config(route_name='families_localized', renderer='langworld_db_pyramid:templates/families.jinja2')
@view_config(route_name='doculects_for_map_family', renderer='json')
def view_families(request):

    family_man_id = request.matchdict['family_man_id']

    if family_man_id == MATCHDICT_ID_FOR_ALL_FAMILIES:
        parent = None
        families = request.dbsession.scalars(select(models.Family).where(models.Family.parent == parent)).all()
    else:
        parent = request.dbsession.scalars(select(models.Family).where(models.Family.man_id == family_man_id)).one()
        families = parent.children
        # TODO top level doculects

    # TODO return 404 if family ID invalid?

    families_with_doculects_that_have_feature_profiles = [f for f in families if f.has_doculects_with_feature_profiles]

    # the point is to provide icons only for the top-level children
    icon_for_family = icon_for_object([parent] + families_with_doculects_that_have_feature_profiles)

    if request.matched_route.name in ('families', 'families_localized'):
        return {
            'parent': parent,
            'families': families_with_doculects_that_have_feature_profiles,
            'icon_for_family': icon_for_family
        }

    # Processing JSON route

    doculects = []

    # TODO this repeats below
    if parent is not None:
        for doculect in [d for d in parent.doculects if d.has_feature_profile]:
            doculects.append(
                {
                    "id": doculect.man_id,
                    "name": getattr(doculect, f'name_{request.locale_name}'),
                    "latitude": doculect.latitude,
                    "longitude": doculect.longitude,
                    "divIconHTML": icon_for_family[parent].svg_tag,
                    "divIconSize": [40, 40],
                    "popupText": (
                        f'<a href="../doculect/{doculect.man_id}">{getattr(doculect, "name_" + request.locale_name)}'
                        f'</a><br/>({getattr(parent, "name_" + request.locale_name)})'
                    ),
                }
            )

    # TODO add doculects that belong to the parent directly!
    for family in families_with_doculects_that_have_feature_profiles:
        for doculect in family.iter_doculects_that_have_feature_profiles():
            # TODO this partly repeats feature.py, can I factor this out?
            doculects.append(
                {
                    "id": doculect.man_id,
                    "name": getattr(doculect, f'name_{request.locale_name}'),
                    "latitude": doculect.latitude,
                    "longitude": doculect.longitude,
                    "divIconHTML": icon_for_family[family].svg_tag,
                    "divIconSize": [40, 40],
                    "popupText": (
                        f'<a href="../doculect/{doculect.man_id}">{getattr(doculect, "name_" + request.locale_name)}'
                        f'</a><br/>({getattr(family, "name_" + request.locale_name)})'
                    ),
                }
            )

    return doculects
