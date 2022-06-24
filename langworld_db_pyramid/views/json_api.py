from pyramid.view import view_config
from sqlalchemy import or_, select

import langworld_db_pyramid.models as models


@view_config(route_name='doculect_man_ids_containing_substring', renderer='json')
def get_man_ids_of_doculects_containing_substring(request):
    locale, query = request.matchdict['locale'], request.matchdict['query']

    # TODO return URLs too?
    return request.dbsession.scalars(
        select(models.Doculect.man_id).where(
            or_(
                getattr(models.Doculect, f'name_{locale}').contains(query),
                getattr(models.Doculect, f'aliases_{locale}').contains(query),
            )
        )
    ).all()
