def includeme(config):
    config.add_static_view('css', 'static/css', cache_max_age=3600)
    config.add_static_view('img', 'static/images', cache_max_age=3600)
    config.add_static_view('scripts', 'static/js', cache_max_age=3600)

    config.add_route('all_doculects_list', '/doculects/list')
    config.add_route('all_doculects_list_localized', '{locale}/doculects/list')

    config.add_route('all_doculects_map', '/doculects/map')
    config.add_route('all_doculects_map_localized', '{locale}/doculects/map')

    config.add_route('doculect_profile', '/doculect/{doculect_man_id}')
    config.add_route('doculect_profile_localized', '{locale}/doculect/{doculect_man_id}')

    config.add_route('doculects_by_substring', '/{locale}/json_api/doculect_by_name/{query}')
    config.add_route('doculects_for_map_all', '/{locale}/json_api/doculects_for_map/all')
    config.add_route('doculects_for_map_feature', '/{locale}/json_api/doculects_for_map/feature/{feature_man_id}')
    config.add_route('genealogy_json', '/{locale}/json_api/genealogy')

    config.add_route('all_features_list', '/features/list')
    config.add_route('all_features_list_localized', '{locale}/features/list')

    config.add_route('feature', '/feature/{feature_man_id}')
    config.add_route('feature_localized', '{locale}/feature/{feature_man_id}')

    config.add_route('families', '/family/{family_man_id}')
    config.add_route('families_localized', '{locale}/family/{family_man_id}')
    config.add_route('doculects_for_map_family', '/{locale}/json_api/doculects_for_map/family/{family_man_id}')

    config.add_route('query_wizard', '/query_wizard')
    config.add_route('query_wizard_localized', '{locale}/query_wizard')
    config.add_route('query_wizard_json', '{locale}/json_api/query_wizard')

    config.add_route('mapbox_token', '/json_api/mapbox_token')
