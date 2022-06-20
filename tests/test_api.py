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


# @pytest.fixture()
def test_get_quiz(client):
    id = '123'
    name = 'TestApi'
    result = client.get(f'/api/get_quiz', query_string= {"name":name,"id":id})
    result_json = result.data.decode('utf8').replace("'", '"')
    import json
    data = json.loads(result_json)
    assert data == [{"answer": "4", "options": ["2", "3", "4", "5"], "question": "What is 2 + 2?"}, {"answer": "a", "options": ["a", "b", "cd", "d"], "question": "dasd"}]
