from pydantic import BaseModel

class PaymentRequest(BaseModel):
    amount_to_deduct: int


class CreditCard():

    def __init__(self, budget, card_id):
        self.budget = budget
        self.card_id = card_id

    def deduct(self, amount_to_deduct):
        self.budget = self.budget - amount_to_deduct


class CreditCardRepo:

    ITEMS = {
        'a': {
            'budget': 500,
            'card_id': 'a'
        },
        'b': {
            'budget': 900,
            'card_id': 'b'
        }
    }

    def get_item_by_card_id(self, card_id):
        card_data = self.ITEMS.get(card_id, {
            'budget': 200,
            'card_id': 'fake_id'
        })
        return CreditCard(**card_data)
         