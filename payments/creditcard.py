from pydantic import BaseModel
import graphene

class CreditCardObject(graphene.ObjectType):
    budget = graphene.Int()
    card_id = graphene.ID()

    def deduct(self, amount_to_deduct):
        self.budget = self.budget - amount_to_deduct


class CreateCreditCard(graphene.Mutation):
    # specify inputs
    class Arguments:
        initial_budget = graphene.Int()
        card_id = graphene.String()

    # specify outputs
    creditcard = graphene.Field(CreditCardObject)

    def mutate(root, info, initial_budget, card_id):
        repo = CreditCardRepo().get_item_by_card_id("a")
        creditcard = CreditCardObject(budget=initial_budget, card_id=card_id)
        return CreateCreditCard(creditcard=creditcard)


class PaymentRequest(BaseModel):
    amount_to_deduct: int


class CreditCard():

    def __init__(self, budget, card_id):
        self.budget = budget
        self.card_id = card_id

    def deduct(self, amount_to_deduct):
        self.budget = self.budget - amount_to_deduct



class CreditCardRepo:

    def __init__(self) -> None:
        self.items = [CreditCardObject(card_id=card_id, budget=budget) for card_id, budget in list(zip(["a", "b", "c"], [500, 900, 200]))]

    def get_item_by_card_id(self, card_id):
        creditcard = [item for item in self.items if item.card_id == card_id][0]
        return creditcard
    
    def get_all_cards(self):
        return self.items         

    def create(self, initial_budget):
        new_creditcard = CreditCardObject(budget=initial_budget, card_id="z")
        self.items.append(new_creditcard) 
        return new_creditcard 