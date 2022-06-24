from langworld_db_pyramid.views.default import view_all_doculects
from langworld_db_pyramid.views.notfound import notfound_view


def test_view_all_doculects_success(dummy_request, test_db_initializer):
    test_db_initializer.setup_models()

    info = view_all_doculects(dummy_request)
    assert dummy_request.response.status_int == 200
    assert len(info['doculects']) == 429
    assert info['project'] == 'Languages of the World Database'


def test_notfound_view(dummy_request):
    info = notfound_view(dummy_request)
    assert dummy_request.response.status_int == 404
    assert info == {}
