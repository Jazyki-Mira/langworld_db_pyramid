from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from .. import models


@view_config(route_name='genealogy', renderer='langworld_db_pyramid:templates/all_families_tree_and_map.jinja2')
@view_config(
    route_name='genealogy_localized', renderer='langworld_db_pyramid:templates/all_families_tree_and_map.jinja2'
)
def view_genealogy(request):
    return {}
