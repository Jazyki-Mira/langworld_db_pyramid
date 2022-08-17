from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy import and_, or_, select
from sqlalchemy.exc import SQLAlchemyError

from .. import models


@view_config(route_name='all_doculects_list', renderer='langworld_db_pyramid:templates/all_doculects_list.jinja2')
@view_config(route_name='all_doculects_list_localized', renderer='langworld_db_pyramid:templates/all_doculects_list.jinja2')
def view_all_doculects_list(request):
    try:
        all_doculects = request.dbsession.scalars(
            select(models.Doculect)
            .where(models.Doculect.has_feature_profile)
            .order_by(getattr(models.Doculect, f'name_{request.locale_name}'))
        ).all()
    except SQLAlchemyError:
        return Response('Database error', content_type='text/plain', status=500)

    try:
        volumes = request.dbsession.scalars(
            select(models.EncyclopediaVolume)
            .order_by(models.EncyclopediaVolume.id)
        ).all()  # TODO test
    except SQLAlchemyError:
        return Response('Database error', content_type='text/plain', status=500)

    return {'doculects': all_doculects, 'volumes': volumes}


@view_config(route_name='doculects_by_substring', renderer='json')
def get_doculects_by_substring(request):
    locale, query = request.locale_name, request.matchdict['query']
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
