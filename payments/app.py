from fastapi import FastAPI
from .creditcard import CreditCardRepo, PaymentRequest

app = FastAPI()

@app.post('/payments/{card_id}')
def deduct_amount_from_creditcard(card_id: str, payment_request: PaymentRequest):
    repo = CreditCardRepo()
    card = repo.get_item_by_card_id(card_id=card_id)
    card.deduct(amount_to_deduct=payment_request.amount_to_deduct)
    return {"budget": card.budget}
