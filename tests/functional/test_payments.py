import graphene
import pytest
from fastapi.testclient import TestClient
from payments.app import Query, app
from payments.creditcard import Payment, PaymentsSystem
from payments.orm import Base, engine, get_db
from payments.entities import CreditCardEntity, CreditCardObject
from payments.repo import CreditCardRepoSQLImpl, CreditRepoInterface


@pytest.fixture
def creditcard_repo(): 
    Base.metadata.create_all(bind=engine)
    yield CreditCardRepoSQLImpl(session=get_db()) 
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def initialized_repo(creditcard_repo: CreditRepoInterface):
    sender_card = CreditCardEntity(budget=900)
    sender_card = creditcard_repo.add(card=sender_card)
    receiver_card = CreditCardEntity(budget=500)
    receiver_card = creditcard_repo.add(card=receiver_card)
    return creditcard_repo

def test_add_creditcard_sql(creditcard_repo: CreditRepoInterface):
    card = CreditCardEntity(budget=20)
    creditcard_repo.add(card)
    card = CreditCardEntity(budget=30)
    creditcard_repo.add(card)
    assert len(creditcard_repo.get_all()) == 2

def test_make_payment(initialized_repo: CreditRepoInterface):
    
    sender_card, receiver_card = initialized_repo.get_all()
    payment = Payment(card_receiver_id=receiver_card.id, card_sender_id=sender_card.id, amount=50)
    payment_system = PaymentsSystem(repo=initialized_repo)
    payment_system.make_payment(payment=payment)
    all_cards = initialized_repo.get_all()
    assert len(all_cards) == 2
    assert initialized_repo.get(receiver_card.id).budget == 550
    assert initialized_repo.get(sender_card.id).budget == 850
