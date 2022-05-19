import pytest


class TestReadAllDriversAPI:
    @pytest.mark.anyio(params=['asyncio'])
    async def test_api_works_correctly(self, create_two_drivers, async_client):
        response = await async_client.get('/drivers/')
        driver1, driver2 = create_two_drivers
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json() == [
            {
                'id': driver1.id,
                'first_name': 'Lewis',
                'last_name': 'Hamilton',
                'number': 44
            },
            {
                'id': driver2.id,
                'first_name': 'Max',
                'last_name': 'Verstappen',
                'number': 1
            }
        ]


class TestReadDriverAPI:
    @pytest.mark.anyio
    async def test_read_driver_api_works(self, create_two_drivers, async_client):
        driver1, driver2 = create_two_drivers
        response = await async_client.get(f'/drivers/{driver2.id}')
        assert response.status_code == 200
        assert response.json() == {
            'id': driver2.id,
            'first_name': 'Max',
            'last_name': 'Verstappen',
            'number': 1
        }


class TestCreateDriverAPI:
    @pytest.mark.anyio
    async def test_admin_can_create_driver(self, create_superuser, async_client):
        payload = {'username': 'admin', 'password': '1234'}
        response = await async_client.post('/token', data=payload)
        token_data = response.json()
        headers = {'Authorization': f'Bearer {token_data.get("access_token")}',
                   'Content-Type': 'application/json'}
        response = await async_client.get('/drivers/')
        assert response.json() == []
        response = await async_client.post('/drivers/',
                                           json={
                                               'first_name': 'Lando',
                                               'last_name': 'Norris',
                                               'number': 5
                                           },
                                           headers=headers)
        assert response.status_code == 201

    @pytest.mark.anyio
    async def test_create_driver_api_validations_check(self, create_superuser, async_client):
        payload = {'username': 'admin', 'password': '1234'}
        response = await async_client.post('/token', data=payload)
        token_data = response.json()
        headers = {'Authorization': f'Bearer {token_data.get("access_token")}',
                   'Content-Type': 'application/json'}
        response = await async_client.post('/drivers/',
                                           json={
                                               'first_name': '1234567890123456789012345',
                                               'last_name': 'sample',
                                               'number': 10
                                           },
                                           headers=headers)
        assert response.status_code == 422

        response = await async_client.post('/drivers/',
                                           json={
                                               'first_name': 'sample',
                                               'last_name': 'sample',
                                               'number': 100
                                           },
                                           headers=headers)
        assert response.status_code == 422

        response = await async_client.post('/drivers/',
                                           json={
                                               'last_name': 'sample',
                                               'number': 100
                                           },
                                           headers=headers)
        assert response.status_code == 422

    @pytest.mark.anyio
    async def test_not_admin_user_cant_create_new_driver(self, create_two_teams_and_user, async_client):
        payload = {'username': 'user', 'password': '1234'}
        response = await async_client.post('/token', data=payload)
        token_data = response.json()
        headers = {'Authorization': f'Bearer {token_data.get("access_token")}',
                   'Content-Type': 'application/json'}
        response = await async_client.post('/drivers/',
                                           json={
                                               'first_name': 'Lando',
                                               'last_name': 'Norris',
                                               'number': 10
                                           },
                                           headers=headers)
        assert response.status_code == 403
        assert response.json() == {'detail': 'Only moderator can create new driver'}


class TestUpdateDriverAPI:
    @pytest.mark.anyio
    async def test_admin_can_update_driver(self, create_two_drivers, create_superuser, async_client):
        driver1, driver2 = create_two_drivers
        payload = {'username': 'admin', 'password': '1234'}
        response = await async_client.post('/token', data=payload)
        token_data = response.json()
        headers = {'Authorization': f'Bearer {token_data.get("access_token")}',
                   'Content-Type': 'application/json'}
        response = await async_client.put(f'/drivers/{driver1.id}',
                                          json={
                                              'first_name': 'Lando',
                                              'last_name': 'Norris',
                                              'number': 10
                                          },
                                          headers=headers)
        assert response.status_code == 200


class TestDeleteDriverAPI:
    @pytest.mark.anyio
    async def test_only_admin_can_delete_driver(self,
                                                create_two_drivers,
                                                create_superuser,
                                                create_user,
                                                async_client):
        driver1, driver2 = create_two_drivers
        admin_payload = {'username': 'admin', 'password': '1234'}
        response = await async_client.post('/token', data=admin_payload)
        admin_token_data = response.json()
        admin_headers = {'Authorization': f'Bearer {admin_token_data.get("access_token")}',
                         'Content-Type': 'application/json'}

        user_payload = {'username': 'user', 'password': '1234'}
        response = await async_client.post('/token', data=user_payload)
        user_token_data = response.json()
        user_headers = {'Authorization': f'Bearer {user_token_data.get("access_token")}',
                        'Content-Type': 'application/json'}

        response = await async_client.delete(f'/drivers/{driver1.id}]', headers=user_headers)
        assert response.status_code == 403

        response = await async_client.delete(f'/drivers/{driver1.id}', headers=admin_headers)
        assert response.status_code == 200
