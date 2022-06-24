from langworld_db_pyramid.models.doculect import Doculect
from langworld_db_pyramid.views.doculects import view_all_doculects, view_doculect_profile
from langworld_db_pyramid.views.notfound import notfound_view


def test_view_all_doculects_success(dummy_request, test_db_initializer):
    test_db_initializer.setup_models()

    info = view_all_doculects(dummy_request)
    assert dummy_request.response.status_int == 200
    assert len(info['doculects']) == 429
    assert info['project'] == 'Languages of the World Database'


def test_view_doculect_profile(dummy_request, test_db_initializer):
    test_db_initializer.setup_models()
    dummy_request.matchdict['doculect_man_id'] = 'aragonese'

    info = view_doculect_profile(dummy_request)
    doculect = info['doculect']
    assert isinstance(doculect, Doculect)
    assert doculect.name_en == 'Aragonese'


def test_notfound_view(dummy_request):
    info = notfound_view(dummy_request)
    assert dummy_request.response.status_int == 404
    assert info == {}
