from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from .. import models


@view_config(route_name='doculect_profile', renderer='langworld_db_pyramid:templates/doculect_profile.jinja2')
@view_config(route_name='doculect_profile_localized', renderer='langworld_db_pyramid:templates/doculect_profile.jinja2')
def view_doculect_profile(request):
    try:
        doculect = request.dbsession.scalars(
            select(models.Doculect).where(models.Doculect.man_id == request.matchdict['doculect_man_id'])
        ).one()
    except SQLAlchemyError:
        return Response('Database error', content_type='text/plain', status=500)

    return {'doculect': doculect}
