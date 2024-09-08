from collections.abc import Iterable
from typing import Any

from pyramid.request import Request
from pyramid.view import view_config
from sqlalchemy import select

from langworld_db_data.constants.literals import ID_SEPARATOR
from langworld_db_pyramid import models
from langworld_db_pyramid.dbutils.query_helpers import get_all
from langworld_db_pyramid.locale.in_code_translation_strings import (
    VISIBLE_MATCHING_DOCULECTS_HEADING,
)
from langworld_db_pyramid.maputils.marker_icons import generate_one_icon
from langworld_db_pyramid.maputils.markers import generate_marker_group
from langworld_db_pyramid.models.feature_value import COMPOUND_VALUE_DELIMITER
from langworld_db_pyramid.views import (
    UNION_VALUE_DELIMITER_IN_QUERY_STRING,
    localized_name_case_insensitive,
)


@view_config(
    route_name="query_wizard", renderer="langworld_db_pyramid:templates/query_wizard.jinja2"
)
@view_config(
    route_name="query_wizard_localized",
    renderer="langworld_db_pyramid:templates/query_wizard.jinja2",
)
def view_query_wizard(request: Request) -> dict[str, Any]:
    return {
        "categories": _get_feature_categories_with_sorted_listed_values(request),
        "families": get_all(
            request, select(models.Family).where(models.Family.parent is None)
        ),  # noqa: E711
    }


def _get_feature_categories_with_sorted_listed_values(
    request: Request,
) -> tuple[dict[str, Any], ...]:
    """Return feature categories with feature values prepared for query wizard.

    1. Filtering: only listed values with doculects remain in categories
    2. Sorting: in multiselect features, elementary values precede compound ones.
       Compound ones are sorted by number of elements.

    Because of potential deepcopy issues (known issue is test failing because of deepcopy),
    we return dictionaries instead of objects. This also allows to only pass to the template
    the attributes that are actually needed there.
    """
    categories: Iterable[models.FeatureCategory] = get_all(request, select(models.FeatureCategory))

    prepared_categories: list[dict[str, Any]] = []

    for category in categories:
        # instead of creating a deepcopy of the object
        # (that e.g. makes tests fail because of deepcopy issues),
        # prepare a dictionary with only the attributes that the Jinja template needs.
        prepared_category = {
            "man_id": category.man_id,
            "name_en": category.name_en,
            "name_ru": category.name_ru,
            "features": [],
        }

        for feature in category.features:
            prepared_feature = {
                "man_id": feature.man_id,
                "name_en": feature.name_en,
                "name_ru": feature.name_ru,
                "values": [],
            }

            listed_values_with_doculects = [
                value for value in feature.values if value.is_listed_and_has_doculects
            ]

            # sort first by complexity, then by integer index of first element of compound value
            # (or the only element if value is simple)

            listed_values_with_doculects.sort(
                key=lambda value: (
                    len(value.elements),
                    int(value.man_id.split(COMPOUND_VALUE_DELIMITER)[0].split(ID_SEPARATOR)[-1]),
                )
            )

            prepared_feature["values"] = [
                {
                    "man_id": value.man_id,
                    "name_en": value.name_en,
                    "name_ru": value.name_ru,
                }
                for value in listed_values_with_doculects
            ]

            prepared_category["features"].append(prepared_feature)

        prepared_categories.append(prepared_category)

    return tuple(prepared_categories)


@view_config(route_name="query_wizard_json", renderer="json")
def get_matching_doculects(request: Request) -> list[dict[str, Any]]:
    locale = request.locale_name

    doculects = get_all(
        request, select(models.Doculect).where(models.Doculect.has_feature_profile)
    )
    icon = generate_one_icon()

    params = {
        key: value.split(UNION_VALUE_DELIMITER_IN_QUERY_STRING)
        for key, value in request.params.items()
    }

    if not params:
        # for uniformity, I return not a dictionary, but a list consisting of one dictionary
        return [
            generate_marker_group(
                request,
                group_id="",
                group_name=request.localizer.translate(VISIBLE_MATCHING_DOCULECTS_HEADING),
                doculects=sorted(doculects, key=localized_name_case_insensitive(locale)),
                div_icon_html=icon.svg_tag,
                img_src=icon.img_src,
            )
        ]

    try:
        family_man_ids = params.pop("family")
    except KeyError:
        matching_doculects = set(doculects)
    else:
        matching_doculects = set()
        for family_id in family_man_ids:
            matching_doculects.update(d for d in doculects if d.belongs_to_family(family_id))

    # every feature has to produce an INTERSECTION with previously found doculects
    for feature_id in params:
        matching_doculects.intersection_update(
            _get_doculects_for_one_feature(
                request=request, parsed_params=params, feature_id=feature_id, doculects=doculects
            )
        )

    return [
        generate_marker_group(
            request,
            group_id="",
            group_name=request.localizer.translate(VISIBLE_MATCHING_DOCULECTS_HEADING),
            div_icon_html=icon.svg_tag,
            img_src=icon.img_src,
            doculects=sorted(matching_doculects, key=localized_name_case_insensitive(locale)),
        )
    ]


def _get_doculects_for_one_feature(
    request: Request,
    parsed_params: dict[str, list[str]],
    feature_id: str,
    doculects: Iterable[models.Doculect],
) -> set[models.Doculect]:
    """Gets matching documents for a given feature.

    If multiple values are given in a request, returns UNION of doculects with any of the values.

    However, for each **compound** value of these potentially multiple values,
    produces INTERSECTION of doculects for this compound value's elements,
    then applies UNION operation with other values.
    """
    doculects_for_feature: set[models.Doculect] = set()

    for value_id in parsed_params[feature_id]:
        doculects_for_value: set[models.Doculect] = set()

        if COMPOUND_VALUE_DELIMITER not in value_id:
            # "normal", non-compound value
            value = models.FeatureValue.get_by_man_id(request=request, man_id=value_id)
            doculects_for_value = {d for d in doculects if d in value.doculects}

        else:
            # This is a compound value.  Get INTERSECTION of doculects for all atomic values
            # to get a set of doculects that have all atomic values.
            for atomic_value_id in value_id.split(COMPOUND_VALUE_DELIMITER):
                atomic_value = models.FeatureValue.get_by_man_id(
                    request=request, man_id=atomic_value_id
                )
                if not doculects_for_value:  # processing first atomic value in the loop
                    doculects_for_value = {d for d in doculects if d in atomic_value.doculects}
                else:
                    doculects_for_value.intersection_update(
                        d for d in doculects if d in atomic_value.doculects
                    )

        doculects_for_feature.update(doculects_for_value)

    return doculects_for_feature
