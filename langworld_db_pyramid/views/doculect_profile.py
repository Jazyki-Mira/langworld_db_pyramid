from pyramid.view import view_config
from sqlalchemy import select

from langworld_db_pyramid import models
from langworld_db_pyramid.dbutils.query_helpers import get_all, get_by_man_id


@view_config(route_name='doculect_profile', renderer='langworld_db_pyramid:templates/doculect.jinja2')
@view_config(route_name='doculect_profile_localized', renderer='langworld_db_pyramid:templates/doculect.jinja2')
def view_doculect_profile(request):
    doculect = get_by_man_id(request=request, model=models.Doculect, man_id=request.matchdict['doculect_man_id'])

    # Create a dictionary to easily find an info item for a given feature value and a given doculect:
    # 1. Query to find info items only for this doculect
    info_items: list[models.DoculectFeatureValueInfo] = get_all(
        request,
        select(models.DoculectFeatureValueInfo).where(models.DoculectFeatureValueInfo.doculect_id == doculect.id))
    # 2. Map feature values to info item for this doculect.
    info_for_feature_value: dict[str, models.DoculectFeatureValueInfo] = {
        item.feature_value: item for item in info_items
    }

    return {
        'doculect': doculect,
        'categories': get_all(request,
                              select(models.FeatureCategory).order_by(models.FeatureCategory.man_id)),
        'info_for_feature_value': info_for_feature_value
    }
