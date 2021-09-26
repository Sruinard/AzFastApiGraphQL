import graphene
from .creditcard import CreditCardObject, CreditCardRepoImpl, CreateCreditCard, MakePayment

class Query(graphene.ObjectType):
    all_creditcards = graphene.List(CreditCardObject)
    creditcard = graphene.Field(CreditCardObject, card_id=graphene.String())

    def resolve_all_creditcards(parent, info):
        return CreditCardRepoImpl().get_all_cards()

    def resolve_creditcard(parent, info, card_id):
        return CreditCardRepoImpl().get(card_id)

class Mutation(graphene.ObjectType):
    
    create_creditcard = CreateCreditCard.Field()

    make_payment = MakePayment.Field()
