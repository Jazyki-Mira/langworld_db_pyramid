from pyramid.view import view_config
from sqlalchemy import select

from langworld_db_pyramid import models
from langworld_db_pyramid.dbutils.query_helpers import get_all, get_by_man_id


@view_config(route_name='doculect_profile', renderer='langworld_db_pyramid:templates/doculect.jinja2')
@view_config(route_name='doculect_profile_localized', renderer='langworld_db_pyramid:templates/doculect.jinja2')
def view_doculect_profile(request):
    return {
        'doculect': get_by_man_id(request=request, model=models.Doculect, man_id=request.matchdict['doculect_man_id']),
        'categories': get_all(request, select(models.FeatureCategory).order_by(models.FeatureCategory.man_id))
    }
