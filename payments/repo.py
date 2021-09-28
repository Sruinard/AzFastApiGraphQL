from typing import List
from payments.entities import CreditCardObject
import payments.models as models

ITEMS = [CreditCardObject(card_id=card_id, budget=budget) for card_id, budget in list(zip(["a", "b", "c"], [500, 900, 200]))]

class CreditRepoInterface:

    def get(self, id):
        raise NotImplementedError 

    def get_cards(self, ids: List[str]):
        raise NotImplementedError

    def get_all_cards(self):
        raise NotImplementedError

    def add(self, card: CreditCardObject):
        raise NotImplementedError

    def update_all(self, items: List[CreditCardObject]):
        raise NotImplementedError

class CreditCardRepoImpl(CreditRepoInterface):

    def get(self, id):
        return [item for item in ITEMS if item.card_id == id][0]

    def get_cards(self, ids):
        cards = [item for item in ITEMS if item.card_id in ids]
        return cards

    def get_all_cards(self):
        return ITEMS

    def add(self, card: CreditCardObject):
        ITEMS.append(card)
        return card

    def update_all(self, items):
        for item_to_update in items:
            for index, item in enumerate(ITEMS):
                if item_to_update.card_id == item.card_id:
                    ITEMS[index] = item_to_update
        return items

class CreditCardRepoSQLImpl(CreditRepoInterface):

    def __init__(self, session):
        self.session = session

    def get(self, id):
        card = self.session.query(models.CreditCard).filter(models.CreditCard.id == id).first()
        return card
    
    def get_all(self):
        cards = self.session.query(models.CreditCard).all()
        return cards

    def add(self, card: CreditCardObject):
        creditcard = models.CreditCard(**card.dict())
        self.session.add(creditcard)
        self.session.commit()
        return creditcard


