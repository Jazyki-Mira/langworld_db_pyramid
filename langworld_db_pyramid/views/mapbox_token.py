from pyramid.view import view_config


@view_config(route_name='mapbox_token', renderer='json')
def get_mapbox_token(request) -> str:
    return request.registry.settings['mapbox_access_token']
