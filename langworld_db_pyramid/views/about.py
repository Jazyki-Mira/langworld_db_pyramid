from typing import Any

from pyramid.request import Request
from pyramid.view import view_config


@view_config(route_name="about", renderer="langworld_db_pyramid:templates/about.jinja2")
@view_config(route_name="about_localized", renderer="langworld_db_pyramid:templates/about.jinja2")
def about(request: Request) -> dict[Any, Any]:  # noqa: ARG001
    return {}
