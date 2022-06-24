def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('all_doculects', '/')
    config.add_route('doculect_profile', '/doculect/{doculect_man_id}')
    config.add_route('doculect_man_ids_containing_substring', '/{locale}/json_api/doculect_by_name/{query}')
