from pyramid.config import Configurator

from langworld_db_pyramid.locale.locale_negotiator import locale_negotiator_from_url


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    with Configurator(settings=settings, locale_negotiator=locale_negotiator_from_url) as config:
        config.include("pyramid_jinja2")
        config.include(".routes")
        config.include(".models")
        config.scan()

        config.add_translation_dirs("langworld_db_pyramid:locale/")
    return config.make_wsgi_app()
