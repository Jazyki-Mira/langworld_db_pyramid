from typing import Union

from pyramid.request import Request
from pyramid.view import view_config
from sqlalchemy import and_, or_, select

from langworld_db_pyramid import models
from langworld_db_pyramid.dbutils.query_helpers import get_all
from langworld_db_pyramid.models import Doculect, EncyclopediaVolume
from langworld_db_pyramid.views import localized_name_case_insensitive


@view_config(
    route_name="all_doculects_list",
    renderer="langworld_db_pyramid:templates/all_doculects_list.jinja2",
)
@view_config(
    route_name="all_doculects_list_localized",
    renderer="langworld_db_pyramid:templates/all_doculects_list.jinja2",
)
def view_all_doculects_list(
    request: Request,
) -> dict[str, list[Union[Doculect, EncyclopediaVolume]]]:
    doculects = get_all(
        request, select(models.Doculect).where(models.Doculect.has_feature_profile)
    )

    volumes = get_all(
        request, select(models.EncyclopediaVolume).order_by(models.EncyclopediaVolume.id)
    )

    return {
        # TODO this case insensitive sorting is repeated in several views.
        #  Should something be included in Doculect model itself?
        "doculects": sorted(doculects, key=localized_name_case_insensitive(request.locale_name)),
        "volumes": volumes,
    }


@view_config(route_name="doculects_by_substring", renderer="json")
def get_doculects_by_substring(request: Request) -> list[dict[str, Union[list[str], str]]]:
    locale, query = request.locale_name, request.matchdict["query"]
    name_attr = f"name_{locale}"
    aliases_attr = f"aliases_{locale}"

    matching_doculects = get_all(
        request,
        select(models.Doculect)
        # Outer join is needed because there are doculects that have no glottocode/ISO-639-3 code.
        # I explicitly state onclause because of many-to-many relationships.
        .join(models.Glottocode, onclause=models.Doculect.glottocodes, isouter=True)
        .join_from(
            models.Doculect,
            models.Iso639P3Code,
            onclause=models.Doculect.iso_639p3_codes,
            isouter=True,
        )
        .where(
            and_(models.Doculect.has_feature_profile),
            or_(
                getattr(models.Doculect, name_attr).contains(query),
                getattr(models.Doculect, aliases_attr).contains(query),
                models.Glottocode.code.contains(query),
                models.Iso639P3Code.code.contains(query),
            ),
        )
        .distinct(),
    )

    return [
        {
            "id": doculect.man_id,
            "name": getattr(doculect, name_attr),
            "aliases": getattr(doculect, aliases_attr),
            "iso639p3Codes": [code.code for code in doculect.iso_639p3_codes],
            "glottocodes": [code.code for code in doculect.glottocodes],
        }
        for doculect in sorted(
            matching_doculects, key=localized_name_case_insensitive(request.locale_name)
        )
    ]
