from collections.abc import Callable
from typing import Any, Union

from pyramid.request import Request

from langworld_db_pyramid.models import Doculect

ID_TO_SHOW_ALL_DOCULECTS = "_all"

UNION_VALUE_DELIMITER_IN_QUERY_STRING = ","


def get_doculect_from_params(request: Request) -> Union[Doculect, None]:
    """Gets Doculect object by ID mentioned in URL param `?show_doculect=...`.
    Returns `None` if URL params do not contain this key.
    """
    try:
        return Doculect.get_by_man_id(request, request.params["show_doculect"])
    except KeyError:
        return None


def localized_name_case_insensitive(locale: str) -> Callable[[Any], str]:
    """Function to be used as key to sort doculects by name in case-insensitive mode."""
    return lambda x: getattr(x, f"name_{locale}").lower()
