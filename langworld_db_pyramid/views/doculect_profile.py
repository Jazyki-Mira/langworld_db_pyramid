from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from .. import models


@view_config(route_name='doculect_profile', renderer='langworld_db_pyramid:templates/doculect.jinja2')
@view_config(route_name='doculect_profile_localized', renderer='langworld_db_pyramid:templates/doculect.jinja2')
def view_doculect_profile(request):
    doculect_man_id = request.matchdict['doculect_man_id']
    try:
        doculect = request.dbsession.scalars(
            select(models.Doculect).where(models.Doculect.man_id == doculect_man_id)
        ).one()
    except SQLAlchemyError:
        raise HTTPNotFound(f"Doculect with ID {doculect_man_id} does not exist")

    categories = request.dbsession.scalars(
        select(models.FeatureCategory).order_by(models.FeatureCategory.man_id)
    ).all()

    return {'doculect': doculect, 'categories': categories}
