from fastapi.testclient import TestClient
import graphene
import pytest
from payments.app import app, Query
from payments.repo import CreditRepoInterface, CreditCardRepoSQLImpl
from payments.creditcard import Payment, PaymentsSystem
from payments.entities import CreditCardObject, CreditCardEntity
from payments.database import get_db
from payments.database import Base, engine

@pytest.fixture
def creditcard_repo():

    ITEMS = [CreditCardObject(card_id=card_id, budget=budget) for card_id, budget in list(zip(["a", "b", "c"], [500, 900, 200]))]

    class CreditCardRepoImpl(CreditRepoInterface):

        def get(self, id):
            return [item for item in ITEMS if item.card_id == id][0]

        def get_cards(self, ids):
            cards = [item for item in ITEMS if item.card_id in ids]
            return cards

        def get_all(self):
            return ITEMS

        def add(self, card: CreditCardObject):
            ITEMS.append(card)

        def update_all(self, items):
            for item_to_update in items:
                for index, item in enumerate(ITEMS):
                    if item_to_update.card_id == item.card_id:
                        ITEMS[index] = item_to_update
            return items

    return CreditCardRepoImpl()

@pytest.fixture
def creditcard_repo_sql(): 
    Base.metadata.create_all(bind=engine)
    yield CreditCardRepoSQLImpl(session=get_db()) 
    Base.metadata.drop_all(bind=engine)

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
    result = CLIENT.post("/graphql", json={"query": query}).json()
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
    result = CLIENT.post("/graphql", json={"query": query}).json()
    assert result["data"]['creditcard'] == {"budget": 500, "cardId": "a"}


def test_create_creditcard():
    query = '''
        mutation MakePayment {
            makePayment(senderId: "a", receiverId: "b", amount: 20) { 
                senderCard { 
                    budget 
                    cardId
                } 
                receiverCard { 
                    budget 
                    cardId
                } 
            }
        }
    '''
    result = CLIENT.post("/graphql", json={"query": query}).json()
    assert result["data"]["makePayment"]['senderCard'] == {"budget": 480, "cardId": "a"}
    assert result["data"]["makePayment"]['receiverCard'] == {"budget": 920, "cardId": "b"}

def test_make_payment(creditcard_repo: CreditRepoInterface):
    
    payment = Payment(card_receiver_id="a", card_sender_id="b", amount=50)
    payment_system = PaymentsSystem(repo=creditcard_repo)
    payment_system.make_payment(payment=payment)
    assert creditcard_repo.get("a").budget == 550
    assert creditcard_repo.get("b").budget == 850

def test_add_creditcard(creditcard_repo: CreditRepoInterface):
    card = CreditCardObject(budget=20, card_id='z')
    creditcard_repo.add(card)
    assert len(creditcard_repo.get_all()) == 4

def test_add_creditcard_sql(creditcard_repo_sql: CreditRepoInterface):
    card = CreditCardEntity(budget=20)
    creditcard_repo_sql.add(card)
    card = CreditCardEntity(budget=20)
    creditcard_repo_sql.add(card)
    assert len(creditcard_repo_sql.get_all()) == 2

def test_add_creditcard_to_database(creditcard_repo_sql: CreditRepoInterface):
    creditcard = CreditCardEntity(budget=100)
    creditcard = creditcard_repo_sql.add(card=creditcard)
    assert creditcard.id is not None
    assert creditcard.budget == 100