from langworld_db_pyramid import models
from langworld_db_pyramid.views.default import view_all_doculects
from langworld_db_pyramid.views.notfound import notfound_view


# def test_view_all_doculects_failure(app_request):
#     info = view_all_doculects(app_request)
#     assert info.status_int == 500

# def test_view_all_doculects_success(dummy_request, dbsession):
#     model = models.Doculect(
#         man_id='english',
#         type='language',
#         is_extinct=False,
#         is_multiple=False,
#         name_en='English',
#         name_ru='английский',
#         custom_title_en='',
#         custom_title_ru='',
#         aliases_en='American English, British English',
#         aliases_ru='британский, американский',
#         family_id='germ',
#         iso_639_3='eng',
#         glottocode='nucl1234',
#         latitude='0.0',
#         longitude='0.0',
#         main_country_id='gbr',
#         encyclopedia_volume_id='10',
#         page='1',
#         has_feature_profile=True,
#         comment='Testing'
#     )
#     dbsession.add(model)
#     dbsession.flush()
#
#     info = view_all_doculects(dummy_request)
#     assert dummy_request.response.status_int == 200
#     assert info['doculects'][0].man_id == 'english'
#     assert len(info['doculects']) == 1
#     assert info['project'] == 'Languages of the World Database'

def test_notfound_view(dummy_request):
    info = notfound_view(dummy_request)
    assert dummy_request.response.status_int == 404
    assert info == {}
