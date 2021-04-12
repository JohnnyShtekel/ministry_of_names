import json

CITIZEN_URL = '/api/v1/ministry_of_names/citizen'
mimetype = 'application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
}


def test_citizen_register(test_client):
    new_citizen = {
        'first_name': "Johnny",
        'last_name': "Shtekel"

    }

    response = _try_register_citizen(new_citizen, test_client)
    _assert_successful_register(new_citizen, response)


def test_citizen_register_same_first_name_validation(test_client):
    new_citizen = {
        'first_name': "Johnny",
        'last_name': "Shtekel"

    }

    response_for_first_citizen = _try_register_citizen(new_citizen, test_client)
    _assert_successful_register(new_citizen, response_for_first_citizen)

    new_citizen_with_similar_name = {
        'first_name': "Johnny",
        'last_name': "Due"

    }

    response_citizen_with_similar_name = _try_register_citizen(new_citizen_with_similar_name, test_client)

    _assert_register_failed(response_citizen_with_similar_name, new_citizen_with_similar_name)


def test_citizen_register_one_edit_distance_validation(test_client):
    new_citizen = {
        'first_name': "Johnny",
        'last_name': "Shtekel"

    }

    response_for_first_citizen = _try_register_citizen(new_citizen, test_client)

    _assert_successful_register(new_citizen, response_for_first_citizen)

    new_citizen_with_similar_name = {
        'first_name': "johnn",
        'last_name': "Due"

    }

    response_citizen_with_similar_name = _try_register_citizen(new_citizen_with_similar_name, test_client)
    _assert_register_failed(response_citizen_with_similar_name, new_citizen_with_similar_name)


def test_citizen_register_one_edit_distance_validation_diffrent_char(test_client):
    new_citizen = {
        'first_name': "Johnny",
        'last_name': "Shtekel"

    }

    response_for_first_citizen = _try_register_citizen(new_citizen, test_client)
    assert response_for_first_citizen.status_code == 201
    assert response_for_first_citizen.json["message"] == f'citizen {new_citizen["first_name"].lower()} registered'

    similar_different_char = {
        'first_name': "Gohnny",
        'last_name': "Due"

    }

    response_citizen_with_similar_name = _try_register_citizen(similar_different_char, test_client)
    _assert_register_failed(response_citizen_with_similar_name, similar_different_char)


def test_serach_for_citizen_by_prefix(test_client):
    search_prefix = "l"

    new_citizen_lists_ids = ["Lior", "Leonid", "Lee", "Lewys", "David"]

    for first_name in new_citizen_lists_ids:
        new_citizen = {"first_name": first_name, "last_name": "Lawrence"}
        response = _try_register_citizen(new_citizen, test_client)
        _assert_successful_register(new_citizen, response)

    response = _search_citizen_by_prefix(search_prefix, test_client)

    citizens = response.json["citizens"]

    expected_search_out_put = set(new_citizen_lists_ids[:-1])

    for citizen in citizens:
        assert citizen["first_name"] in expected_search_out_put


def _search_citizen_by_prefix(prefix, test_client):
    response = test_client.get(f"{CITIZEN_URL}?first_name={prefix}")
    return response


def _try_register_citizen(citizen, test_client):
    response = test_client.post(CITIZEN_URL, data=json.dumps(citizen), headers=headers)
    return response


def _assert_register_failed(response, citizen):
    assert response.status_code == 409
    assert response.json[
               "error"] == f'the name {citizen["first_name"].lower()} is similar up to one editing distance'


def _assert_successful_register(citizen, response):
    assert response.status_code == 201
    assert response.json["message"] == f'citizen {citizen["first_name"].lower()} registered'
