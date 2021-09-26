import graphene
from .creditcard import CreditCardObject, CreditCardRepo, CreateCreditCard, MakePayment

class Query(graphene.ObjectType):
    all_creditcards = graphene.List(CreditCardObject)
    creditcard = graphene.Field(CreditCardObject, card_id=graphene.String())

    def resolve_all_creditcards(parent, info):
        return CreditCardRepo().get_all_cards()

    def resolve_creditcard(parent, info, card_id):
        return CreditCardRepo().get_item_by_card_id(card_id)

class Mutation(graphene.ObjectType):
    create_creditcard = CreateCreditCard.Field()
    make_payment = MakePayment.Field()
