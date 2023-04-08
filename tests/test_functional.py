import pytest


def test_notfound(testapp, setup_models_once_for_test_module):
    res = testapp.get("/badurl", status=404)
    assert res.status_code == 404


@pytest.mark.parametrize(
    "url, expected_strings",
    [
        ("/doculects/list", ["французский", "английский", "русский", "группировкой по томам"]),
        ("/ru/doculects/list", ["французский", "английский", "русский", "группировкой по томам"]),
        ("/en/doculects/list", ["French", "English", "Russian", "by encyclopedia volume"]),
        (
            "/doculect/french",
            [
                "французский язык",
                "Том 11. Романские языки",
                "stan1290",
                "fra</a>",
                "Признаки",
                "doculects/map?",
            ],
        ),
        (
            "/ru/doculect/french",
            [
                "французский язык",
                "Том 11. Романские языки",
                "stan1290",
                "fra</a>",
                "Признаки",
                "doculects/map?",
            ],
        ),
        (
            "/en/doculect/french",
            [
                "French",
                "Volume 11. Romance languages",
                "stan1290",
                "fra</a>",
                "Features",
                "doculects/map?",
            ],
        ),
        ("/features/list", [">Фонемный состав</h2>"]),
        ("/feature/G-2", ["Маркирование единственного числа"]),
        ("/ru/feature/G-2", ["Маркирование единственного числа"]),
        ("/en/feature/A-9", ["Diphthongs and triphthongs"]),
        ("/ru/features/list", [">Слог</h2>"]),
        ("/en/features/list", [">Syllable</h2>"]),
        ("/ru/family/_all", ["Все языки"]),
        ("/ru/family/altai", ["Алтайские языки"]),
        ("/ru/query_wizard", ["Форма запроса"]),
        ("/", ["База данных"]),
        ("/ru/home", ["База данных"]),
        ("/en/home", ["Database"]),
    ],
)
def test_doculect(testapp, setup_models_once_for_test_module, url, expected_strings):
    res = testapp.get(url, status=200)
    for str_ in expected_strings:
        assert str_ in res
