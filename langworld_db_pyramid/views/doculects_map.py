from typing import Any, Optional

from pyramid.request import Request
from pyramid.view import view_config
from sqlalchemy import select

from langworld_db_pyramid import models
from langworld_db_pyramid.dbutils.query_helpers import get_all
from langworld_db_pyramid.locale.in_code_translation_strings import ALL_VISIBLE_DOCULECTS_HEADING
from langworld_db_pyramid.maputils.marker_icons import generate_one_icon
from langworld_db_pyramid.maputils.markers import generate_marker_group
from langworld_db_pyramid.views import get_doculect_from_params, localized_name_case_insensitive


@view_config(
    route_name="all_doculects_map",
    renderer="langworld_db_pyramid:templates/all_doculects_map.jinja2",
)
@view_config(
    route_name="all_doculects_map_localized",
    renderer="langworld_db_pyramid:templates/all_doculects_map.jinja2",
)
def view_all_doculects_map(request: Request) -> dict[str, Optional[models.Doculect]]:
    return {"doculect_in_focus": get_doculect_from_params(request)}


@view_config(route_name="doculects_for_map_all", renderer="json")
def get_doculects_for_map(request: Request) -> list[dict[str, Any]]:
    doculects = get_all(
        request, select(models.Doculect).where(models.Doculect.has_feature_profile)
    )

    icon = generate_one_icon()

    # for uniformity, I return not a dictionary, but a list consisting of one dictionary
    return [
        generate_marker_group(
            request,
            group_id="",
            group_name=request.localizer.translate(ALL_VISIBLE_DOCULECTS_HEADING),
            doculects=sorted(doculects, key=localized_name_case_insensitive(request.locale_name)),
            div_icon_html=icon.svg_tag,
            img_src=icon.img_src,
        )
    ]
