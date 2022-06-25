import pytest as pytest

from __init__ import create_app


@pytest.fixture()
def client():
    application = create_app()
    with application.test_client() as client:
        with application.app_context():
            from extensions import db
            db.init_app(application)
        yield client


def test_get_quiz(client):
    id = '666'
    name = 'TestApi'
    result = client.get('/api/get_quiz', query_string={"name": name, "id": id})
    result_json = result.data.decode('utf8').replace("'", '"')
    import json
    print(result_json)
    data = json.loads(result_json)
    assert data == [{"answer": "A", "options": ["A", "B", "C", "D"], "question": "tes"},
                    {"answer": "A", "options": ["A", "B", "C", "D"], "question": "tes"}]


def test_get_result(client):
    id = '666'
    name = 'TestApi'
    result = client.get('/api/get_result', query_string={"id": id, "name": name})
    result_json = result.data.decode('utf8').replace("'", '"')
    import json
    data = json.loads(result_json)
    assert data == {
        "correct_answers": 0,
        "percentage": 100.0,
        "points": 0,
        "status": "success"
    }


def test_close_quiz(client):
    id = '666'
    result = client.get('/api/close_quiz', query_string={"id": id})
    result_json = result.data.decode('utf8').replace("'", '"')
    import json
    data = json.loads(result_json)
    assert data == {
        "status": "success"
    }


