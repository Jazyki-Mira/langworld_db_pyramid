from pyramid.view import view_config
from sqlalchemy import select

from langworld_db_pyramid import models
from langworld_db_pyramid.locale.in_code_translation_strings import ALL_VISIBLE_DOCULECTS_HEADING
from langworld_db_pyramid.maputils.marker_icons import generate_one_icon
from langworld_db_pyramid.maputils.markers import generate_marker_group


@view_config(route_name='all_doculects_map', renderer='langworld_db_pyramid:templates/all_doculects_map.jinja2')
@view_config(route_name='all_doculects_map_localized',
             renderer='langworld_db_pyramid:templates/all_doculects_map.jinja2')
def view_all_doculects_map(request):
    return {}


@view_config(route_name='doculects_for_map_all', renderer='json')
def get_doculects_for_map(request) -> list[dict]:

    doculects = request.dbsession.scalars(select(models.Doculect).where(models.Doculect.has_feature_profile)).all()
    icon = generate_one_icon()

    # for uniformity, I return not a dictionary, but a list consisting of one dictionary
    return [
        generate_marker_group(
            group_id='',
            group_name=request.localizer.translate(ALL_VISIBLE_DOCULECTS_HEADING),
            doculects=sorted(doculects, key=lambda d: getattr(d, f'name_{request.locale_name}')),
            div_icon_html=icon.svg_tag,
            img_src=icon.img_src,
            locale=request.locale_name,
        )
    ]
