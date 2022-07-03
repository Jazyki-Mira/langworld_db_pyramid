from pyramid.view import view_config
from sqlalchemy import or_, select

import langworld_db_pyramid.models as models


@view_config(route_name='doculect_man_ids_containing_substring', renderer='json')
def get_man_ids_of_doculects_containing_substring(request):
    locale, query = request.matchdict['locale'], request.matchdict['query']
    name_attr = f'name_{locale}'
    aliases_attr = f'aliases_{locale}'

    # TODO Search by ISO, glottocode?
    matching_doculects = request.dbsession.scalars(
        select(models.Doculect).where(
            or_(
                getattr(models.Doculect, name_attr).contains(query),
                getattr(models.Doculect, aliases_attr).contains(query),
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
