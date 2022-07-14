from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from .. import models
from langworld_db_pyramid.maputils.generate_map_icons import icon_for_object


@view_config(route_name='feature', renderer='langworld_db_pyramid:templates/feature.jinja2')
@view_config(route_name='feature_localized', renderer='langworld_db_pyramid:templates/feature.jinja2')
@view_config(route_name='doculects_for_map_feature', renderer='json')
def view_feature(request):
    try:
        feature = request.dbsession.scalars(
            select(models.Feature).where(models.Feature.man_id == request.matchdict['feature_man_id'])
        ).one()
    except SQLAlchemyError:
        return Response('Database error', content_type='text/plain', status=500)

    values = sorted(
        [value for value in feature.values if value.type.name == 'listed' and value.doculects],
        key=lambda value: (len(value.doculects), value.id), reverse=True
    )
    icon_for_value = icon_for_object(values)

    if request.matched_route.name in ('feature', 'feature_localized'):
        return {
            'feature_name': getattr(feature, f'name_{request.locale_name}'),
            'man_id': feature.man_id,
            'values': values,
            'icon_for_value': icon_for_value
        }
    elif request.matched_route.name == 'doculects_for_map_feature':
        data = []
        for value in values:
            for doculect in value.doculects:
                data.append(
                    {
                        "id": doculect.man_id,
                        "name": getattr(doculect, f'name_{request.locale_name}'),
                        "latitude": doculect.latitude,
                        "longitude": doculect.longitude,
                        "divIconHTML": icon_for_value[value].svg_tag,
                        "divIconSize": [40, 40],
                        "popupText": (
                            f'<a href="../doculect/{doculect.man_id}">{getattr(doculect, "name_" + request.locale_name)}'
                            f'</a><br/>({getattr(feature, "name_" + request.locale_name)}: '
                            f'{getattr(value, "name_" + request.locale_name)})'
                        ),
                    }
                )
        return data
    else:
        return Response(f'Route {request.matched_route.name} is not supported', content_type='text/plain', status=500)

    # TODO not adding tests yet because I might use React to do entire feature profile
