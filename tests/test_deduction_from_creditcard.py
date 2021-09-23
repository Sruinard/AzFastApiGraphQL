from fastapi.testclient import TestClient
import graphene

from payments.creditcard import CreditCard
from payments.app import app, QueryPerson


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


def test_query_person_data():
    schema = graphene.Schema(query=QueryPerson)
    result = schema.execute('''
        {
            me(name: "Stef") { firstName lastName}
            myBestFriend { firstName lastName }
            allCreditcards { budget }
        }
    ''')
    # With default resolvers we can resolve attributes from an object..
    assert result.data["me"] == {"firstName": "Stef", "lastName": "Skywalker"}

    # With default resolvers, we can also resolve keys from a dictionary..
    assert result.data["myBestFriend"] == {"firstName": "R2", "lastName": "D2"}

    assert result.data["allCreditcards"] == [{"budget": 500}, {"budget": 900}, {"budget": 200}]