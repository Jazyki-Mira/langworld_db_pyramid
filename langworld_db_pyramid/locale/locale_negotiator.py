from pyramid.settings import aslist

DEFAULT_LOCALE = 'ru'


def locale_negotiator_from_url(request):
    if not request.matchdict:
        return DEFAULT_LOCALE

    locale = request.matchdict.get('locale', 'ru')

    if locale not in aslist(request.registry.settings['available_languages']):
        return DEFAULT_LOCALE

    return locale
