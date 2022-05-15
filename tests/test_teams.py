class TestReadAllTeamsAPI:
    def test_read_all_teams_api_works_correctly(self, create_two_teams_and_user, client):
        response = client.get('/teams/')
        assert response.status_code == 200
        assert len(response.json()) == 2


class TestReadTeamAPI:
    def test_read_team_api_works_correctly(self, create_two_teams_and_user, client):
        response = client.get('/teams/2')
        assert response.status_code == 200
        assert response.json().get('id') == 2


class TestCreateTeamAPI:
    def test_create_team_api_by_logged_user_works(self, create_two_teams_and_user, client):
        response = client.get('/teams/')
        assert len(response.json()) == 2

        payload = {'username': 'user', 'password': '1234'}
        response = client.post('/token', data=payload)
        token_data = response.json()
        headers = {'Authorization': f'Bearer {token_data.get("access_token")}',
                   'Content-Type': 'application/json'}

        response = client.post('/teams/',
                               json={'name': 'test team'},
                               headers=headers)
        assert response.status_code == 201

        response = client.get('/teams/')
        assert len(response.json()) == 3

    def test_create_team_api_by_not_logged_user_doesnt_work(self, create_two_teams_and_user, client):
        response = client.get('/teams/')
        assert len(response.json()) == 2
        response = client.post('/teams/',
                               json={
                                   'name': 'test team'
                               })
        assert response.status_code == 401
