from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from .. import models


@view_config(route_name='all_doculects_map', renderer='langworld_db_pyramid:templates/all_doculects_map.jinja2')
@view_config(route_name='all_doculects_map_localized', renderer='langworld_db_pyramid:templates/all_doculects_map.jinja2')
def view_all_doculects(request):
    try:
        all_doculects = request.dbsession.scalars(
            select(models.Doculect).order_by(getattr(models.Doculect, f'name_{request.locale_name}'))
        ).all()
    except SQLAlchemyError:
        return Response('Database error', content_type='text/plain', status=500)

    return {'doculects': all_doculects}
