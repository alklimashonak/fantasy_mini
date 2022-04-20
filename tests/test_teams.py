def test_read_all_teams_api_valid(create_two_teams, client):
    response = client.get('/teams')
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json() == [
        {
            'id': 1,
            'name': 'team 1',
            'owner_id': 1
        },
        {
            'id': 2,
            'name': 'team 2',
            'owner_id': 1
        },
    ]


def test_read_team_api_valid(create_two_teams, client):
    response = client.get('/teams/2')
    assert response.status_code == 200
    assert response.json() == {
        'id': 2,
        'name': 'team 2',
        'drivers': [],
        'owner_id': 1
    }


def test_create_team_api(create_two_teams, client):
    response = client.get('/teams')
    assert len(response.json()) == 2
    client.post('/teams?user_id=1',
                json={
                    'name': 'test team'
                })
    response = client.get('/teams')
    assert len(response.json()) == 3
