from typing import Union
from pyramid.request import Request

from langworld_db_pyramid.models import Doculect


def get_doculect_from_params(request: Request) -> Union[Doculect, None]:
    """Gets Doculect object by ID mentioned in URL param `?show_doculect=...`.
    Returns `None` if URL params do not contain this key.
    """
    try:
        return Doculect.get_by_man_id(request, request.params['show_doculect'])
    except KeyError:
        return
