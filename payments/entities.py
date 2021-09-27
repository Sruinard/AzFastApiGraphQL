import graphene

class CreditCardObject(graphene.ObjectType):
    budget = graphene.Int()
    card_id = graphene.ID()

    def add_payment(self, amount):
        self.budget = self.budget - amount