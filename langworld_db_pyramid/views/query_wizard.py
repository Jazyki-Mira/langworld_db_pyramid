from pyramid.view import view_config
from sqlalchemy import select

from langworld_db_pyramid import models
from langworld_db_pyramid.dbutils.query_helpers import get_all
from langworld_db_pyramid.locale.in_code_translation_strings import VISIBLE_MATCHING_DOCULECTS_HEADING
from langworld_db_pyramid.maputils.marker_icons import generate_one_icon
from langworld_db_pyramid.maputils.markers import generate_marker_group


@view_config(route_name='query_wizard', renderer='langworld_db_pyramid:templates/query_wizard.jinja2')
@view_config(route_name='query_wizard_localized', renderer='langworld_db_pyramid:templates/query_wizard.jinja2')
def view_query_wizard(request):
    return {
        'categories': get_all(request, select(models.FeatureCategory)),
        'families': get_all(request, select(models.Family).where(models.Family.parent == None))  # noqa: E711
    }


@view_config(route_name='query_wizard_json', renderer='json')
def get_matching_doculects(request) -> list[dict]:
    name_attr = f'name_{request.locale_name}'

    doculects = get_all(request, select(models.Doculect).where(models.Doculect.has_feature_profile))
    icon = generate_one_icon()

    params = {key: value.split(',') for key, value in request.params.items()}

    if not params:
        # for uniformity, I return not a dictionary, but a list consisting of one dictionary
        return [
            generate_marker_group(
                request,
                group_id='',
                group_name=request.localizer.translate(VISIBLE_MATCHING_DOCULECTS_HEADING),
                doculects=sorted(doculects, key=lambda d: getattr(d, name_attr)),
                div_icon_html=icon.svg_tag,
                img_src=icon.img_src,
            )
        ]

    try:
        family_man_ids = params['family']
    except KeyError:
        matching_doculects = set(doculects)
    else:
        matching_doculects = set()
        for family_id in family_man_ids:
            matching_doculects.update(d for d in doculects if d.belongs_to_family(family_id))
        del params['family']

    # every feature has to be an intersection, while every value within a feature has to be a union
    for feature_id in params:
        doculects_with_any_of_requested_values_of_feature: set[models.Doculect] = set()
        for value_id in params[feature_id]:
            value = models.FeatureValue.get_by_man_id(request=request, man_id=value_id)
            doculects_with_any_of_requested_values_of_feature.update(d for d in doculects if d in value.doculects)

        matching_doculects.intersection_update(doculects_with_any_of_requested_values_of_feature)

    return [
        generate_marker_group(
            request,
            group_id='',
            group_name=request.localizer.translate(VISIBLE_MATCHING_DOCULECTS_HEADING),
            div_icon_html=icon.svg_tag,
            img_src=icon.img_src,
            doculects=sorted(matching_doculects, key=lambda d: getattr(d, name_attr)),
        )
    ]
