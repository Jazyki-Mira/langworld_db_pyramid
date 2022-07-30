from pyramid.view import view_config
from sqlalchemy import select

from .. import models
from langworld_db_pyramid.maputils.generate_map_icons import generate_fixed_number_of_map_icons
from langworld_db_pyramid.maputils.marker import generate_marker


@view_config(route_name='query_wizard', renderer='langworld_db_pyramid:templates/query_wizard.jinja2')
@view_config(
    route_name='query_wizard_localized', renderer='langworld_db_pyramid:templates/query_wizard.jinja2'
)
def view_query_wizard(request):
    return {
        'categories': request.dbsession.scalars(select(models.FeatureCategory)).all(),
        'families': request.dbsession.scalars(select(models.Family).where(models.Family.parent == None)).all()
    }


@view_config(route_name='query_wizard_json', renderer='json')
def get_matching_doculects(request):
    # TODO test

    doculects = set(
        request.dbsession.scalars(
            select(models.Doculect).where(models.Doculect.has_feature_profile)
        ).all()
    )
    icon = generate_fixed_number_of_map_icons(1)

    params = {key: value.split(',') for key, value in request.params.items()}

    if not params:
        return [
            generate_marker(request=request, doculect=doculect, div_icon_html=icon.svg_tag)
            for doculect in doculects
        ]

    print(params)

    try:
        family_man_ids = params['family']
    except KeyError:
        matching_doculects = doculects.copy()
    else:
        matching_doculects = set()
        for family_id in family_man_ids:
            matching_doculects.update(d for d in doculects if d.belongs_to_family(family_id))
        del params['family']

    # every feature has to be an intersection, while every value within a feature has to be a union
    for feature_id in params:
        doculects_with_any_of_requested_values_of_feature = set()
        for value_id in params[feature_id]:
            value = request.dbsession.scalars(
                select(models.FeatureValue).where(models.FeatureValue.man_id == value_id)
            ).one()
            doculects_with_any_of_requested_values_of_feature.update(d for d in doculects if d in value.doculects)

        matching_doculects.intersection_update(doculects_with_any_of_requested_values_of_feature)

    return [
        generate_marker(request=request, doculect=doculect, div_icon_html=icon.svg_tag)
        for doculect in matching_doculects
    ]
