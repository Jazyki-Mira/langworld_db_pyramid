from pyramid.request import Request
from pyramid.view import view_config


@view_config(route_name="mapbox_token", renderer="json")
def get_mapbox_token(request: Request) -> str:
    # value will be taken from `mapbox_access_token` key of `[app:main]` section in `.ini` file
    return request.registry.settings["mapbox_access_token"]
