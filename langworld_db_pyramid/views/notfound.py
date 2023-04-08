from pyramid.view import notfound_view_config


@notfound_view_config(renderer="langworld_db_pyramid:templates/404.jinja2")
def notfound_view(request):
    request.response.status = 404

    # This view is not registered in routes.py. This means that the common locale negotiator
    # will not determine the English locale correctly because there is no `matchdict`
    # from which English locale can be extracted.
    # There may be a better solution, but it seems easy to just check the relative URL.
    # It will only stop working if I change the URL system completely.
    if request.path.startswith("/en/"):
        request.locale_name = "en"

    return {}
