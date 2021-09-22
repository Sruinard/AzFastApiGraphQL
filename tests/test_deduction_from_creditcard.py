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

def test_graph_endpoint():
    query= """
    {
        hello(name: "FastApi")
    }
    """
    result = CLIENT.post("/graph", json={"query": query})
    assert "Hello" in result.json().get("data").get('hello')