class TestReadAllDriversAPI:
    def test_api_works_correctly(self, create_two_drivers, client):
        response = client.get('/drivers')
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json() == [
            {
                'id': create_two_drivers[0].id,
                'first_name': 'Lewis',
                'last_name': 'Hamilton',
                'number': 44
            },
            {
                'id': create_two_drivers[1].id,
                'first_name': 'Max',
                'last_name': 'Verstappen',
                'number': 1
            }
        ]


class TestReadDriverAPI:
    def test_read_driver_api_works(self, create_two_drivers, client):
        response = client.get(f'/drivers/{create_two_drivers[1].id}')
        assert response.status_code == 200
        assert response.json() == {
            'id': create_two_drivers[1].id,
            'first_name': 'Max',
            'last_name': 'Verstappen',
            'number': 1
        }


class TestCreateDriverAPI:
    def test_admin_can_create_driver(self, create_superuser, client):
        payload = {'username': 'admin', 'password': '1234'}
        response = client.post('/token', data=payload)
        token_data = response.json()
        headers = {'Authorization': f'Bearer {token_data.get("access_token")}',
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

    def test_create_driver_api_validations_check(self, create_superuser, client):
        payload = {'username': 'admin', 'password': '1234'}
        response = client.post('/token', data=payload)
        token_data = response.json()
        headers = {'Authorization': f'Bearer {token_data.get("access_token")}',
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

    def test_not_admin_user_cant_create_new_driver(self, create_two_teams_and_user, client):
        payload = {'username': 'user', 'password': '1234'}
        response = client.post('/token', data=payload)
        token_data = response.json()
        headers = {'Authorization': f'Bearer {token_data.get("access_token")}',
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


class TestUpdateDriverAPI:
    def test_admin_can_update_driver(self, create_two_drivers, create_superuser, client):
        payload = {'username': 'admin', 'password': '1234'}
        response = client.post('/token', data=payload)
        token_data = response.json()
        headers = {'Authorization': f'Bearer {token_data.get("access_token")}',
                   'Content-Type': 'application/json'}
        response = client.put(f'/drivers/{create_two_drivers[0].id}',
                              json={
                                  'first_name': 'Lando',
                                  'last_name': 'Norris',
                                  'number': 10
                              },
                              headers=headers)
        assert response.status_code == 200


class TestDeleteDriverAPI:
    def test_only_admin_can_delete_driver(self,
                                          create_two_drivers,
                                          create_superuser,
                                          create_user,
                                          client):
        admin_payload = {'username': 'admin', 'password': '1234'}
        response = client.post('/token', data=admin_payload)
        admin_token_data = response.json()
        admin_headers = {'Authorization': f'Bearer {admin_token_data.get("access_token")}',
                         'Content-Type': 'application/json'}

        user_payload = {'username': 'user', 'password': '1234'}
        response = client.post('/token', data=user_payload)
        user_token_data = response.json()
        user_headers = {'Authorization': f'Bearer {user_token_data.get("access_token")}',
                        'Content-Type': 'application/json'}

        response = client.delete(f'/drivers/{create_two_drivers[0].id}]', headers=user_headers)
        assert response.status_code == 403

        response = client.delete(f'/drivers/{create_two_drivers[0].id}', headers=admin_headers)
        assert response.status_code == 200
