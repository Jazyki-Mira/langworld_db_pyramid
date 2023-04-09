from pyramid.request import Request
from pyramid.settings import aslist

DEFAULT_LOCALE = "ru"


def locale_negotiator_from_url(request: Request) -> str:
    if not request.matchdict:
        return DEFAULT_LOCALE

    locale: str = request.matchdict.get("locale", "ru")

    if locale not in aslist(request.registry.settings["available_languages"]):
        return DEFAULT_LOCALE

    return locale
