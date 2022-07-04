from pyramid.settings import aslist


def locale_negotiator_from_url(request):
    locale = request.matchdict.get('locale', 'ru')

    if locale not in aslist(request.registry.settings['available_languages']):
        locale = 'ru'

    return locale
