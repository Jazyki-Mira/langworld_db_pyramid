from pyramid.view import view_config
from sqlalchemy import select

from .. import models
from langworld_db_pyramid.maputils.generate_map_icons import generate_fixed_number_of_map_icons


@view_config(route_name='all_doculects_map', renderer='langworld_db_pyramid:templates/all_doculects_map.jinja2')
@view_config(
    route_name='all_doculects_map_localized', renderer='langworld_db_pyramid:templates/all_doculects_map.jinja2'
)
def view_all_doculects_map(request):
    return {}


@view_config(route_name='doculects_for_map_all', renderer='json')
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
            "divIconHTML": generate_fixed_number_of_map_icons(1).svg_tag,
            "divIconSize": [40, 40]
        }
        for doculect in doculects
    ]

    return data
