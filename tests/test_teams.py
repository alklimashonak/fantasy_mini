def test_read_all_teams_api_valid(create_two_teams, client):
    response = client.get('/teams')
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_read_team_api_valid(create_two_teams, client):
    response = client.get('/teams/2')
    assert response.status_code == 200
    assert response.json().get('id') == 2


def test_create_team_api(create_two_teams, client):
    response = client.get('/teams')
    assert len(response.json()) == 2
    client.post('/teams?user_id=1',
                json={
                    'name': 'test team'
                })
    response = client.get('/teams')
    assert len(response.json()) == 3
