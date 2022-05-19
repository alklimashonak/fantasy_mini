import pytest


class TestReadAllTeamsAPI:
    @pytest.mark.anyio
    async def test_read_all_teams_api_works_correctly(self, create_two_teams_and_user, async_client):
        response = await async_client.get('/teams/')
        assert response.status_code == 200
        assert len(response.json()) == 2


class TestReadTeamAPI:
    @pytest.mark.anyio
    async def test_read_team_api_works_correctly(self, create_two_teams_and_user, async_client):
        user, team1, team2 = create_two_teams_and_user
        response = await async_client.get(f'/teams/{team2.id}')
        assert response.status_code == 200
        assert response.json().get('id') == team2.id


class TestCreateTeamAPI:
    @pytest.mark.anyio
    async def test_create_team_api_by_logged_user_works(self, create_two_teams_and_user, async_client):
        response = await async_client.get('/teams/')
        assert len(response.json()) == 2

        payload = {'username': 'user', 'password': '1234'}
        response = await async_client.post('/token', data=payload)
        token_data = response.json()
        headers = {'Authorization': f'Bearer {token_data.get("access_token")}',
                   'Content-Type': 'application/json'}

        response = await async_client.post('/teams/',
                                           json={'name': 'test team'},
                                           headers=headers)
        assert response.status_code == 201

        response = await async_client.get('/teams/')
        assert len(response.json()) == 3

    @pytest.mark.anyio
    async def test_create_team_api_by_not_logged_user_doesnt_work(self, create_two_teams_and_user, async_client):
        response = await async_client.get('/teams/')
        assert len(response.json()) == 2
        response = await async_client.post('/teams/',
                                           json={
                                               'name': 'test team'
                                           })
        assert response.status_code == 401


class TestUpdateTeamAPI:
    @pytest.mark.anyio
    async def test_update_team_api_by_not_logged_user_doesnt_work(self, create_two_teams_and_user, async_client):
        response = await async_client.put(
            '/teams/1',
            json={'name': 'some name'}
        )
        assert response.status_code == 401
        assert response.json() == {'detail': 'Not authenticated'}

    @pytest.mark.anyio
    async def test_user_can_update_only_own_team(self, create_two_teams_and_user, create_superuser, async_client):
        user, team1, team2 = create_two_teams_and_user

        admin_payload = {'username': 'admin', 'password': '1234'}
        user_payload = {'username': 'user', 'password': '1234'}

        admin_login_response = await async_client.post('/token', data=admin_payload)
        admin_token_data = admin_login_response.json()

        user_login_response = await async_client.post('/token', data=user_payload)
        user_token_data = user_login_response.json()

        admin_headers = {'Authorization': f'Bearer {admin_token_data.get("access_token")}',
                         'Content-Type': 'application/json'}
        user_headers = {'Authorization': f'Bearer {user_token_data.get("access_token")}',
                        'Content-Type': 'application/json'}

        admin_response = await async_client.put(
            f'/teams/{team1.id}',
            json={'name': 'some name'},
            headers=admin_headers
        )
        assert admin_response.status_code == 403
        assert admin_response.json() == {'detail': 'You can update only your own team'}

        user_response = await async_client.put(
            f'/teams/{team1.id}',
            json={'name': 'some name'},
            headers=user_headers
        )
        assert user_response.status_code == 200
        assert user_response.json() == {
            'id': team1.id,
            'name': 'some name',
            'owner_id': user.id,
            'drivers': []
        }


class TestDeleteTeamAPI:
    @pytest.mark.anyio
    async def test_delete_team_api_by_not_logged_user_doesnt_work(self, create_two_teams_and_user, async_client):
        user, team1, team2 = create_two_teams_and_user
        response = await async_client.delete(f'/teams/{team1.id}')
        assert response.status_code == 401
        assert response.json() == {'detail': 'Not authenticated'}

    @pytest.mark.anyio
    async def test_user_can_delete_only_own_team(self, create_two_teams_and_user, create_superuser, async_client):
        user, team1, team2 = create_two_teams_and_user

        admin_payload = {'username': 'admin', 'password': '1234'}
        user_payload = {'username': 'user', 'password': '1234'}

        admin_login_response = await async_client.post('/token', data=admin_payload)
        admin_token_data = admin_login_response.json()

        user_login_response = await async_client.post('/token', data=user_payload)
        user_token_data = user_login_response.json()

        admin_headers = {'Authorization': f'Bearer {admin_token_data.get("access_token")}',
                         'Content-Type': 'application/json'}
        user_headers = {'Authorization': f'Bearer {user_token_data.get("access_token")}',
                        'Content-Type': 'application/json'}

        admin_response = await async_client.delete(
            '/teams/1',
            headers=admin_headers
        )
        assert admin_response.status_code == 403
        assert admin_response.json() == {'detail': 'You can delete only your own team'}

        user_response = await async_client.delete(
            f'/teams/{team1.id}',
            headers=user_headers
        )
        assert user_response.status_code == 200
        assert user_response.json() == {
            'id': team1.id,
            'name': team1.name,
            'owner_id': user.id,
            'drivers': []
        }
