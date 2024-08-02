from typing import Any

from pyramid.request import Request
from pyramid.view import view_config


@view_config(route_name="howto", renderer="langworld_db_pyramid:templates/howto.jinja2")
@view_config(route_name="howto_localized", renderer="langworld_db_pyramid:templates/howto.jinja2")
def howto(request: Request) -> dict[Any, Any]:  # noqa: ARG001
    return {}
