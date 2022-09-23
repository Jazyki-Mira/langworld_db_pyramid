from typing import Any

from pyramid.request import Request

from langworld_db_pyramid.dbutils.query_helpers import _get_by_man_id


class QueryMixin:
    """Mixin for performing SQLAlchemy queries.
    All methods are class methods because they operate on 'mapped classes'
    (e.g. models.Doculect) and not instances (e.g. individual doculect).
    """

    @classmethod
    def get_by_man_id(cls, request: Request, man_id: str) -> Any:
        """Accepts a Pyramid request and 'man_id' of the required object
        (e.g. doculect of family). Returns this object
        or raises HTTPNotFound if no object was found.
        """
        return _get_by_man_id(request, cls, man_id)
