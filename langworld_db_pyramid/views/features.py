from collections.abc import Iterable
from typing import Any, Union

from pyramid.request import Request
from pyramid.view import view_config
from sqlalchemy import select

from langworld_db_pyramid import models
from langworld_db_pyramid.dbutils.query_helpers import get_all
from langworld_db_pyramid.locale.in_code_translation_strings import (
    NAME_OF_GROUP_WITH_EMPTY_VALUES_FOR_MAP,
)
from langworld_db_pyramid.maputils.marker_icons import (
    COLOR_FOR_EMPTY_VALUE,
    OPACITY_FOR_EMPTY_VALUE,
    CLLDIcon,
    CLLDPie,
    icon_for_object,
)
from langworld_db_pyramid.maputils.markers import generate_marker_group
from langworld_db_pyramid.views import get_doculect_from_params, localized_name_case_insensitive


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
) -> tuple[
    models.Feature,
    list[models.FeatureValue],
    dict[Any, Union[CLLDIcon, CLLDPie]],
    list[models.FeatureValue],
]:
    feature = models.Feature.get_by_man_id(
        request=request, man_id=request.matchdict["feature_man_id"]
    )

    listed_values = sorted(
        [value for value in feature.values if value.type.name == "listed" and value.doculects],
        key=lambda value: value.id,
    )

    # This will generate icons for all values if feature is regular
    # or for all elementary values if the feature is_multiselect
    icon_for_listed_value = icon_for_object([v for v in listed_values if not v.elements])

    # construct icons for compound values from same colors as the icons of their elements
    for compound_value in [v for v in listed_values if v.elements]:
        colors = []
        for element in compound_value.elements:
            # dotted notation makes mypy complain: CLLDPie has no .color, while CLLDPie is in Union
            colors.append(getattr(icon_for_listed_value[element], "color"))

        icon_for_listed_value[compound_value] = CLLDPie(colors)

    # single list of empty values for group of white markers (single icon will be assigned later)
    empty_values = [
        value
        for value in feature.values
        if value.type.name in ("not_stated", "not_applicable", "explicit_gap") and value.doculects
    ]

    return feature, listed_values, icon_for_listed_value, empty_values


@view_config(route_name="feature", renderer="langworld_db_pyramid:templates/feature.jinja2")
@view_config(
    route_name="feature_localized", renderer="langworld_db_pyramid:templates/feature.jinja2"
)
def view_feature_list_of_values(request: Request) -> dict[str, Any]:
    def _get_sorted_listed_values_for_feature_description(
        values: Iterable[models.FeatureValue],
    ) -> tuple[models.FeatureValue, ...]:
        """Sorts feature values by integer value of `man_id`."""
        values_to_return = [v for v in values if v.type.name == "listed"]
        values_to_return.sort(key=lambda v: int(v.man_id.split("-")[-1]))
        return tuple(values_to_return)

    feature = models.Feature.get_by_man_id(
        request=request, man_id=request.matchdict["feature_man_id"]
    )
    locale = request.locale_name
    return {
        "feature_name": getattr(feature, f"name_{locale}"),
        "man_id": feature.man_id,
        "feature_description": getattr(feature, f"description_html_{locale}"),
        "values": _get_sorted_listed_values_for_feature_description(feature.values),
        "doculect_in_focus": get_doculect_from_params(request),
    }


@view_config(route_name="doculects_for_map_feature", renderer="json")
def view_feature_map_of_values(request: Request) -> list[dict[str, Any]]:
    feature, listed_values, icon_for_listed_value, empty_values = get_feature_values_icons(request)
    locale = request.locale_name
    name_attr = "name_" + locale

    empty_value_icon = CLLDIcon(f"c{COLOR_FOR_EMPTY_VALUE}", opacity=OPACITY_FOR_EMPTY_VALUE)

    return [  # listed values
        generate_marker_group(
            request,
            group_id=value.man_id,
            group_name=getattr(value, name_attr),
            div_icon_html=icon_for_listed_value[value].svg_tag,
            img_src=icon_for_listed_value[value].img_src,
            doculects=sorted(value.doculects, key=localized_name_case_insensitive(locale)),
            additional_popup_text=f"({getattr(feature, name_attr)}: {getattr(value, name_attr)})",
        )
        for value in listed_values
    ] + [
        generate_marker_group(  # one group with single icon for all empty values
            request,
            group_id="empty",
            group_name=request.localizer.translate(NAME_OF_GROUP_WITH_EMPTY_VALUES_FOR_MAP),
            div_icon_html=empty_value_icon.svg_tag,
            doculects=sorted(
                (doculects for value in empty_values for doculects in value.doculects),
                key=localized_name_case_insensitive(locale),
            ),
            img_src=empty_value_icon.img_src,
            additional_popup_text=(
                f"({getattr(feature, name_attr)}: "
                f"{request.localizer.translate(NAME_OF_GROUP_WITH_EMPTY_VALUES_FOR_MAP)}"
            ),
        )
    ]
