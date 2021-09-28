import graphene
import pydantic
from typing import Optional

class CreditCardEntity(pydantic.BaseModel):
    id: Optional[int]
    budget: int


class CreditCardObject(graphene.ObjectType):
    budget = graphene.Int()
    card_id = graphene.ID()

    def add_payment(self, amount):
        self.budget = self.budget - amount