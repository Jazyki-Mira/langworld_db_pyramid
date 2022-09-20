from pyramid.view import view_config
from sqlalchemy import select

from langworld_db_pyramid import models
from langworld_db_pyramid.dbutils.query_helpers import get_all, get_by_man_id


@view_config(route_name='doculect_profile', renderer='langworld_db_pyramid:templates/doculect.jinja2')
@view_config(route_name='doculect_profile_localized', renderer='langworld_db_pyramid:templates/doculect.jinja2')
def view_doculect_profile(request):
    doculect = get_by_man_id(request=request, model=models.Doculect, man_id=request.matchdict['doculect_man_id'])

    # Create a dictionary to easily find a comment for a given feature value and a given doculect:
    # 1. Query to find comments only for this doculect
    comments: list[models.DoculectFeatureValueComment] = get_all(
        request,
        select(models.DoculectFeatureValueComment).where(models.DoculectFeatureValueComment.doculect_id == doculect.id))
    # 2. Map feature values to comments for this doculect.
    comment_for_feature_value: dict[str, models.DoculectFeatureValueComment] = {
        comment.feature_value: comment for comment in comments
    }

    return {
        'doculect': doculect,
        'categories': get_all(request,
                              select(models.FeatureCategory).order_by(models.FeatureCategory.man_id)),
        'comment_for_feature_value': comment_for_feature_value
    }
