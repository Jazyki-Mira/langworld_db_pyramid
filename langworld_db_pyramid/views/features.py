from typing import Any

from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from langworld_db_pyramid import models
from langworld_db_pyramid.dbutils.query_helpers import get_all, get_by_man_id
from langworld_db_pyramid.maputils.marker_icons import CLLDIcon, icon_for_object
from langworld_db_pyramid.maputils.markers import generate_marker_group


@view_config(route_name='all_features_list', renderer='langworld_db_pyramid:templates/all_features_list.jinja2')
@view_config(route_name='all_features_list_localized',
             renderer='langworld_db_pyramid:templates/all_features_list.jinja2')
def view_all_features_list_by_category(request):
    return {'categories': get_all(request, select(models.FeatureCategory))}


def get_feature_values_icons(request) -> tuple[models.Feature, list[models.FeatureValue], dict[Any, CLLDIcon]]:
    feature_man_id = request.matchdict['feature_man_id']
    try:
        feature = get_by_man_id(request=request, model=models.Feature, man_id=feature_man_id)
    except SQLAlchemyError:
        raise HTTPNotFound(f"Feature with ID {feature_man_id} does not exist")

    values = sorted([value for value in feature.values if value.type.name == 'listed' and value.doculects],
                    key=lambda value: (len(value.doculects), value.id),
                    reverse=True)

    return feature, values, icon_for_object(values)


@view_config(route_name='feature', renderer='langworld_db_pyramid:templates/feature.jinja2')
@view_config(route_name='feature_localized', renderer='langworld_db_pyramid:templates/feature.jinja2')
def view_feature_list_of_values(request):
    # The list of values is no longer shown (because it would duplicate the interactive list),
    # but it still makes sense to use the common function
    feature, _, _ = get_feature_values_icons(request)
    return {
        'feature_name': getattr(feature, f'name_{request.locale_name}'),
        'man_id': feature.man_id,
    }


@view_config(route_name='doculects_for_map_feature', renderer='json')
def view_feature_map_of_values(request) -> list[dict]:
    feature, values, icon_for_value = get_feature_values_icons(request)
    locale = request.locale_name
    name_attr = "name_" + locale

    return [
        generate_marker_group(
            group_id=value.man_id,
            group_name=getattr(value, name_attr),
            div_icon_html=icon_for_value[value].svg_tag,
            img_src=icon_for_value[value].img_src,
            doculects=sorted(value.doculects, key=lambda d: getattr(d, name_attr)),
            locale=locale,
            additional_popup_text=f'({getattr(feature, name_attr)}: {getattr(value, name_attr)})',
        ) for value in values
    ]
