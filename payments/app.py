from fastapi import FastAPI
from .creditcard import CreditCard
from .creditcard import CreditCardRepo

app = FastAPI()

@app.post('/payments/{card_id}')
def deduct_amount_from_creditcard(card_id: str, amount_to_deduct: int):
    repo = CreditCardRepo()
    card = repo.get_item_by_card_id(card_id=card_id)
    card.deduct(amount_to_deduct=amount_to_deduct)
    return {"budget": card.budget}
