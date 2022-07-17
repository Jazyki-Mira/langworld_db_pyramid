from pyramid.view import view_config
from sqlalchemy import select

from .. import models
from langworld_db_pyramid.maputils.generate_map_icons import icon_for_object


@view_config(route_name='all_features_list', renderer='langworld_db_pyramid:templates/all_features_list.jinja2')
@view_config(
    route_name='all_features_list_localized', renderer='langworld_db_pyramid:templates/all_features_list.jinja2'
)
def view_all_features_list_by_category(request):
    return {'categories': request.dbsession.scalars(select(models.FeatureCategory)).all()}


def get_feature_values_icons(request):
    feature = request.dbsession.scalars(
        select(models.Feature).where(models.Feature.man_id == request.matchdict['feature_man_id'])
    ).one()

    values = sorted(
        [value for value in feature.values if value.type.name == 'listed' and value.doculects],
        key=lambda value: (len(value.doculects), value.id), reverse=True
    )

    return feature, values, icon_for_object(values)


@view_config(route_name='feature', renderer='langworld_db_pyramid:templates/feature.jinja2')
@view_config(route_name='feature_localized', renderer='langworld_db_pyramid:templates/feature.jinja2')
def view_feature_list_of_values(request):
    feature, values, icon_for_value = get_feature_values_icons(request)
    return {
        'feature_name': getattr(feature, f'name_{request.locale_name}'),
        'man_id': feature.man_id,
        'values': values,
        'icon_for_value': icon_for_value
    }


@view_config(route_name='doculects_for_map_feature', renderer='json')
def view_feature_map_of_values(request):
    feature, values, icon_for_value = get_feature_values_icons(request)
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
