def test_read_all_drivers_api(create_two_drivers, client):
    response = client.get('/drivers')
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json() == [
        {
            'id': 1,
            'first_name': 'Lewis',
            'last_name': 'Hamilton',
            'number': 44
        },
        {
            'id': 2,
            'first_name': 'Max',
            'last_name': 'Verstappen',
            'number': 1
        }
    ]


def test_read_driver_api(create_two_drivers, client):
    response = client.get('/drivers/2')
    assert response.status_code == 200
    assert response.json() == {
        'id': 2,
        'first_name': 'Max',
        'last_name': 'Verstappen',
        'number': 1
    }


def test_create_driver_api(client):
    response = client.get('/drivers')
    assert response.json() == []
    client.post('/drivers', json={
        'first_name': 'Lando',
        'last_name': 'Norris',
        'number': 5
    })
    response = client.get('/drivers')
    assert response.json() == [
        {
            'id': 1,
            'first_name': 'Lando',
            'last_name': 'Norris',
            'number': 5
        }
    ]


def test_create_driver_api_validations_check(client):
    response = client.post('drivers', json={
        'first_name': '1234567890123456789012345',
        'last_name': 'sample',
        'number': 10
    })
    assert response.status_code == 422

    response = client.post('drivers', json={
        'first_name': 'sample',
        'last_name': 'sample',
        'number': 100
    })
    assert response.status_code == 422

    response = client.post('drivers', json={
        'last_name': 'sample',
        'number': 100
    })
    assert response.status_code == 422
