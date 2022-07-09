from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from .. import models


@view_config(route_name='all_features_list', renderer='langworld_db_pyramid:templates/all_features_list.jinja2')
@view_config(
    route_name='all_features_list_localized', renderer='langworld_db_pyramid:templates/all_features_list.jinja2'
)
def view_all_features(request):
    try:
        categories = request.dbsession.scalars(select(models.FeatureCategory)).all()
    except SQLAlchemyError:
        return Response('Database error', content_type='text/plain', status=500)

    return {'categories': categories}
    # TODO simple test
