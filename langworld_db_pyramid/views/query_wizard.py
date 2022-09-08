from gettext import gettext as _

from pyramid.i18n import TranslationString
from pyramid.view import view_config
from sqlalchemy import select

from langworld_db_pyramid import models
from langworld_db_pyramid.maputils.marker_icons import generate_one_icon
from langworld_db_pyramid.maputils.markers import generate_marker_group


@view_config(route_name='query_wizard', renderer='langworld_db_pyramid:templates/query_wizard.jinja2')
@view_config(route_name='query_wizard_localized', renderer='langworld_db_pyramid:templates/query_wizard.jinja2')
def view_query_wizard(request):
    return {
        'categories': request.dbsession.scalars(select(models.FeatureCategory)).all(),
        'families': request.dbsession.scalars(select(models.Family).where(models.Family.parent == None)  # noqa: E711
                                              ).all()
    }


@view_config(route_name='query_wizard_json', renderer='json')
def get_matching_doculects(request) -> list[dict]:
    name_attr = f'name_{request.locale_name}'

    doculects = set(request.dbsession.scalars(select(models.Doculect).where(models.Doculect.has_feature_profile)).all())
    group_name = TranslationString(_('Подходящие языки на видимой области карты'))
    icon = generate_one_icon()

    params = {key: value.split(',') for key, value in request.params.items()}

    if not params:
        # for uniformity, I return not a dictionary, but a list consisting of one dictionary
        return [
            generate_marker_group(
                group_id='',
                group_name=request.localizer.translate(group_name),
                doculects=sorted(doculects, key=lambda d: getattr(d, name_attr)),
                div_icon_html=icon.svg_tag,
                img_src=icon.img_src,
                locale=request.locale_name,
            )
        ]

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
        doculects_with_any_of_requested_values_of_feature: set[models.Doculect] = set()
        for value_id in params[feature_id]:
            value = request.dbsession.scalars(
                select(models.FeatureValue).where(models.FeatureValue.man_id == value_id)).one()
            doculects_with_any_of_requested_values_of_feature.update(d for d in doculects if d in value.doculects)

        matching_doculects.intersection_update(doculects_with_any_of_requested_values_of_feature)

    return [
        generate_marker_group(
            group_id='',
            group_name=request.localizer.translate(group_name),
            div_icon_html=icon.svg_tag,
            img_src=icon.img_src,
            doculects=sorted(matching_doculects, key=lambda d: getattr(d, name_attr)),
            locale=request.locale_name,
        )
    ]
