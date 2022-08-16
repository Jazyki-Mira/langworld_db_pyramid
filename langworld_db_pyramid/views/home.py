from pyramid.view import view_config


@view_config(route_name='home', renderer='langworld_db_pyramid:templates/home.jinja2')
@view_config(route_name='home_localized', renderer='langworld_db_pyramid:templates/home.jinja2')
@view_config(route_name='home_empty', renderer='langworld_db_pyramid:templates/home.jinja2')
def front(request):
    return {}
