from fastapi.testclient import TestClient
import graphene

from payments.app import app, Query, Mutation


CLIENT = TestClient(app)

def test_api_endpoint_is_available():
    response = CLIENT.get('/')
    assert response.json() == "Fast API + GraphQL"


def test_get_all_creditcard_budgets():
    schema = graphene.Schema(query=Query)
    result = schema.execute("""
        query CreditCardQuery {
            allCreditcards { budget }
        }
    """)
    assert result.data["allCreditcards"] == [{"budget": 500}, {"budget": 900}, {"budget": 200}]


def test_create_creditcard():
    query = '''
        mutation CreateCreditCard {
            createCreditcard(initialBudget: 0, cardId: "z") { 
                creditcard { 
                    budget 
                    cardId
                } 
            }
        }
    '''
    result = CLIENT.post("/creditcard", json={"query": query}).json()
    assert result["data"]["createCreditcard"]['creditcard'] == {"budget": 0, "cardId": "z"}

def test_create_creditcard():
    query = '''
        query getCreditcard {
            creditcard(cardId: "a") { 
                    budget 
                    cardId
                } 
        }
    '''
    result = CLIENT.post("/creditcard", json={"query": query}).json()
    assert result["data"]['creditcard'] == {"budget": 500, "cardId": "a"}