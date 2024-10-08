from unittest.mock import patch

@patch('stripe.Charge.create')
def test_payment(mock_charge, client):
    mock_charge.return_value = {'id': 'charge_id'}
    client.post('/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    login_res = client.post('/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    token = login_res.json['token']

    response = client.post('/payment', json={
        'amount': 100,
        'token': 'fake_token'
    }), headers={'x-access-token': token}

    assert response.status_code == 200
    assert response.json['message'] == 'Payment processed successfully'