from pyramid.config import Configurator


def includeme(config: Configurator) -> None:
    config.add_static_view("css", "static/css", cache_max_age=3600)
    config.add_static_view("img", "static/images", cache_max_age=3600)
    config.add_static_view("scripts", "static/js", cache_max_age=3600)
    add_routes_for_page_views_with_i18n(config)
    config.add_route("home_empty", "/")  # '/' and '/home' will lead to the same page

    # JSON for Javascript fetch requests: always with explicit locale except for Mapbox token
    config.add_route("doculects_by_substring", "/{locale}/json_api/doculect_by_name/{query}")
    config.add_route("doculects_for_map_all", "/{locale}/json_api/doculects_for_map/all")
    config.add_route(
        "doculects_for_map_family", "/{locale}/json_api/doculects_for_map/family/{family_man_id}"
    )
    config.add_route(
        "doculects_for_map_feature",
        "/{locale}/json_api/doculects_for_map/feature/{feature_man_id}",
    )
    config.add_route("genealogy_json", "/{locale}/json_api/genealogy")
    config.add_route("query_wizard_json", "/{locale}/json_api/query_wizard")
    config.add_route(
        "mapbox_token", "/json_api/mapbox_token"
    )  # intentionally without locale as it's not needed


def add_routes_for_page_views_with_i18n(config: Configurator) -> None:
    """Adds routes for page views.
    These operations live a separate function so they can be used
    in testing to avoid duplication.
    """
    # routes for Jinja rendering all come in two variations: plain (with implicit default locale)
    # and with explicit locale
    names_and_paths = (
        ("all_doculects_list", "doculects/list"),  # leading slash will be added in the loop
        ("all_doculects_map", "doculects/map"),
        ("doculect_profile", "doculect/{doculect_man_id}"),
        ("all_features_list", "features/list"),
        ("feature", "feature/{feature_man_id}"),
        ("families", "family/{family_man_id}"),
        ("home", "home"),
        ("query_wizard", "query_wizard"),
    )
    for name, path in names_and_paths:
        config.add_route(name, f"/{path}")
        config.add_route(
            f"{name}_localized", "/{locale}/" + path
        )  # no f-string because of curly braces
