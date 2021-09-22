from fastapi import FastAPI
from .creditcard import CreditCardRepo, PaymentRequest
import graphene
from fastapi import FastAPI
from starlette.graphql import GraphQLApp


class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))

    def resolve_hello(self, info, name):
        return "Hello " + name


# app = FastAPI()
app = FastAPI()
app.add_route("/graph", GraphQLApp(schema=graphene.Schema(query=Query)))

@app.get("/")
def homepage():
    return "Fast API + GraphQL"

@app.post('/payments/{card_id}')
def deduct_amount_from_creditcard(card_id: str, payment_request: PaymentRequest):
    repo = CreditCardRepo()
    card = repo.get_item_by_card_id(card_id=card_id)
    card.deduct(amount_to_deduct=payment_request.amount_to_deduct)
    return {"budget": card.budget}
