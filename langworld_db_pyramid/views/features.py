from pyramid.view import view_config
from sqlalchemy import select

from .. import models
from langworld_db_pyramid.maputils.generate_map_icons import icon_for_object
from langworld_db_pyramid.maputils.marker import generate_marker


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
    name_attr = "name_" + request.locale_name

    return [
        generate_marker(
            request, doculect,
            div_icon_html=icon_for_value[value].svg_tag,
            additional_popup_text=f'({getattr(feature, name_attr)}: {getattr(value, name_attr)})'
        )
        for value in values for doculect in value.doculects
    ]

