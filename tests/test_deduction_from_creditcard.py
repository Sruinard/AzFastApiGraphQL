from fastapi.testclient import TestClient

from payments.creditcard import CreditCard
from payments.app import app


CLIENT = TestClient(app)



def test_creditcard_deduct_value():
    creditcard = CreditCard(budget=200, card_id='a')
    creditcard.deduct(150)
    assert creditcard.budget == 50

def test_api_endpoint_is_available():
    response = CLIENT.post('/payments/a', json={'amount_to_deduct': 50})
    assert response.json() == {'budget': 450}