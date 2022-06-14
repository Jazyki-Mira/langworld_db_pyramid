def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('all_doculects', '/')
    # config.add_route('doculect_profile', '/{doculect_str_id}')
