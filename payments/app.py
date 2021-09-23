from fastapi import FastAPI
from .creditcard import CreditCardRepo, PaymentRequest
import graphene
from fastapi import FastAPI
from starlette.graphql import GraphQLApp
from collections import namedtuple

from graphene import ObjectType, String, Field, Schema

PersonValueObject = namedtuple("Person", ["first_name", "last_name"])

class Person(ObjectType):
    first_name = String()
    last_name = String()

class QueryPerson(ObjectType):
    me = Field(Person, name=graphene.String())
    my_best_friend = Field(Person)

    def resolve_me(parent, info, name="Luke"):
        # always pass an object for `me` field
        return PersonValueObject(first_name=name, last_name="Skywalker")

    def resolve_my_best_friend(parent, info):
        # always pass a dictionary for `my_best_fiend_field`
        return {"first_name": "R2", "last_name": "D2"}

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
