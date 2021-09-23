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

    ITEMS = [dict(card_id=card_id, budget=budget) for card_id, budget in list(zip(["a", "b", "c"], [500, 900, 200]))]

    def get_item_by_card_id(self, card_id):
        card_data = [item for item in self.ITEMS if item.get("card_id") == card_id][0]
        return CreditCard(**card_data)
    
    def get_all_cards(self):
        return [CreditCard(**card_data) for card_data in self.ITEMS]
         