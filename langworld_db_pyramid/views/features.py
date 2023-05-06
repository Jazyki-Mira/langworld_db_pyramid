from operator import attrgetter
from typing import Any

from pyramid.request import Request
from pyramid.view import view_config
from sqlalchemy import select

from langworld_db_pyramid import models
from langworld_db_pyramid.dbutils.query_helpers import get_all
from langworld_db_pyramid.maputils.marker_icons import CLLDIcon, icon_for_object
from langworld_db_pyramid.maputils.markers import generate_marker_group
from langworld_db_pyramid.views import get_doculect_from_params


@view_config(
    route_name="all_features_list",
    renderer="langworld_db_pyramid:templates/all_features_list.jinja2",
)
@view_config(
    route_name="all_features_list_localized",
    renderer="langworld_db_pyramid:templates/all_features_list.jinja2",
)
def view_all_features_list_by_category(
    request: Request,
) -> dict[str, list[models.FeatureCategory]]:
    return {"categories": get_all(request, select(models.FeatureCategory))}


def get_feature_values_icons(
    request: Request,
) -> tuple[models.Feature, list[models.FeatureValue], dict[Any, CLLDIcon]]:
    feature = models.Feature.get_by_man_id(
        request=request, man_id=request.matchdict["feature_man_id"]
    )

    # I sort values by number of doculects (descending), but if the number of doculects is
    # the same, I have to sort by value ID (ascending). Hence, this trick with negative value ID
    # (`.id` is auto-incremented integer): reverse sorting by negative value ID de facto produces
    # ascending sorting by original value ID.
    values = sorted(
        [value for value in feature.values if value.type.name == "listed" and value.doculects],
        key=lambda value: (len(value.doculects), -value.id),
        reverse=True,
    )

    return feature, values, icon_for_object(values)


@view_config(route_name="feature", renderer="langworld_db_pyramid:templates/feature.jinja2")
@view_config(
    route_name="feature_localized", renderer="langworld_db_pyramid:templates/feature.jinja2"
)
def view_feature_list_of_values(request: Request) -> dict[str, Any]:
    feature = models.Feature.get_by_man_id(
        request=request, man_id=request.matchdict["feature_man_id"]
    )
    return {
        "feature_name": getattr(feature, f"name_{request.locale_name}"),
        "man_id": feature.man_id,
        "doculect_in_focus": get_doculect_from_params(request),
    }


@view_config(route_name="doculects_for_map_feature", renderer="json")
def view_feature_map_of_values(request: Request) -> list[dict[str, Any]]:
    feature, values, icon_for_value = get_feature_values_icons(request)
    locale = request.locale_name
    name_attr = "name_" + locale

    return [
        generate_marker_group(
            request,
            group_id=value.man_id,
            group_name=getattr(value, name_attr),
            div_icon_html=icon_for_value[value].svg_tag,
            img_src=icon_for_value[value].img_src,
            doculects=sorted(value.doculects, key=attrgetter(name_attr)),
            additional_popup_text=f"({getattr(feature, name_attr)}: {getattr(value, name_attr)})",
        )
        # exclude compound values  # TODO make 2 versions of map
        for value in values
        if not value.elements
        # FIXME labels on popups become incorrect
    ]
