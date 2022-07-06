def includeme(config):
    config.add_static_view('css', 'static/css', cache_max_age=3600)
    config.add_static_view('img', 'static/images', cache_max_age=3600)
    config.add_static_view('scripts', 'static/js', cache_max_age=3600)
    config.add_static_view('pdf', 'static/pdf_volumes', cache_max_age=3600)

    config.add_route('all_doculects_list', '/doculects/list')
    config.add_route('all_doculects_list_localized', '{locale}/doculects/list')

    config.add_route('all_doculects_map', '/doculects/map')
    config.add_route('all_doculects_map_localized', '{locale}/doculects/map')

    config.add_route('doculect_profile', '/doculect/{doculect_man_id}')
    config.add_route('doculect_profile_localized', '{locale}/doculect/{doculect_man_id}')

    config.add_route('doculects_by_substring', '/{locale}/json_api/doculect_by_name/{query}')
    config.add_route('doculects_for_map', '/{locale}/json_api/doculects_for_map/')
