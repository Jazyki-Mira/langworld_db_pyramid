from clldutils import svg
from pyramid.view import view_config
from sqlalchemy import and_, or_, select

import langworld_db_pyramid.models as models


@view_config(route_name='doculects_by_substring', renderer='json')
def get_doculects_by_substring(request):
    locale, query = request.matchdict['locale'], request.matchdict['query']
    name_attr = f'name_{locale}'
    aliases_attr = f'aliases_{locale}'

    # TODO Search by ISO, glottocode?
    matching_doculects = request.dbsession.scalars(
        select(models.Doculect).where(
            and_(
                models.Doculect.has_feature_profile,
                or_(
                    getattr(models.Doculect, name_attr).contains(query),
                    getattr(models.Doculect, aliases_attr).contains(query),
                )
            )
        )
    ).all()

    data = [
        {
            "id": doculect.man_id,
            "name": getattr(doculect, name_attr),
            "aliases": getattr(doculect, aliases_attr),
            "iso639p3Codes": [code.code for code in doculect.iso_639p3_codes],
            "glottocodes": [code.code for code in doculect.glottocodes],
        }
        for doculect in matching_doculects
    ]

    return sorted(data, key=lambda item: item['name'])


@view_config(route_name='doculects_for_map', renderer='json')
def get_doculects_for_map(request):
    locale = request.matchdict['locale']
    name_attr = f'name_{locale}'

    doculects = request.dbsession.scalars(
        select(models.Doculect).where(models.Doculect.has_feature_profile)
    ).all()

    data = [
        {
            "id": doculect.man_id,
            "name": getattr(doculect, name_attr),
            "latitude": doculect.latitude,
            "longitude": doculect.longitude,
            "divIconHTML": svg.icon('c008080'),  # teal circle
            "divIconSize": [40, 40]
        }
        for doculect in doculects
    ]

    return sorted(data, key=lambda item: item['name'])


@view_config(route_name='genealogy_json', renderer='json')
def get_genealogy(request):

    def _get_family_with_children(family: models.Family):
        data = {
            'id': family.man_id,
            'name': getattr(family, name_attr),
            'children': [],
            'doculects': [],
        }

        if family.doculects:
            data['doculects'] = sorted([
                {
                    'id': doculect.man_id,
                    'name': getattr(doculect, name_attr),
                    'latitude': doculect.latitude,
                    'longitude': doculect.longitude,
                }
                for doculect in family.doculects if doculect.has_feature_profile
            ], key=lambda doculect: doculect['name'])

        if family.children:
            data['children'] = [
                _get_family_with_children(child) for child in family.children
                if child.has_doculects_with_feature_profiles()
            ]

        return data

    locale = request.matchdict['locale']
    name_attr = f'name_{locale}'

    # Picking only top families (I must use '==' here because SQLAlchemy will not accept 'is')
    top_level_families = request.dbsession.scalars(
        select(models.Family).where(models.Family.parent == None)
    ).all()

    return [
        _get_family_with_children(family) for family in top_level_families
        if family.has_doculects_with_feature_profiles()
    ]
