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


def test_admin_create_driver_api_works(create_superuser, client):
    headers = {'Authorization': 'Bearer admin',
               'Content-Type': 'application/json'}
    response = client.get('/drivers/')
    assert response.json() == []
    response = client.post('/drivers/',
                           json={
                               'first_name': 'Lando',
                               'last_name': 'Norris',
                               'number': 5
                           },
                           headers=headers)
    assert response.status_code == 201
    response = client.get('/drivers/')
    assert response.json() == [
        {
            'id': 1,
            'first_name': 'Lando',
            'last_name': 'Norris',
            'number': 5
        }
    ]


def test_create_driver_api_validations_check(create_superuser, client):
    headers = {'Authorization': 'Bearer admin',
               'Content-Type': 'application/json'}
    response = client.post('/drivers/',
                           json={
                               'first_name': '1234567890123456789012345',
                               'last_name': 'sample',
                               'number': 10
                           },
                           headers=headers)
    assert response.status_code == 422

    response = client.post('/drivers/',
                           json={
                               'first_name': 'sample',
                               'last_name': 'sample',
                               'number': 100
                           },
                           headers=headers)
    assert response.status_code == 422

    response = client.post('/drivers/',
                           json={
                               'last_name': 'sample',
                               'number': 100
                           },
                           headers=headers)
    assert response.status_code == 422


def test_not_admin_user_cant_create_new_driver(create_two_teams_and_user, client):
    headers = {'Authorization': 'Bearer user',
               'Content-Type': 'application/json'}
    response = client.post('/drivers/',
                           json={
                               'first_name': 'Lando',
                               'last_name': 'Norris',
                               'number': 10
                           },
                           headers=headers)
    assert response.status_code == 403
    assert response.json() == {'detail': 'Only moderator can create new driver'}


def test_admin_can_update_driver(create_two_drivers, create_superuser, client):
    headers = {'Authorization': 'Bearer admin',
               'Content-Type': 'application/json'}
    response = client.put('/drivers/1',
                          json={
                              'first_name': 'Lando',
                              'last_name': 'Norris',
                              'number': 10
                          },
                          headers=headers)
    assert response.status_code == 200
