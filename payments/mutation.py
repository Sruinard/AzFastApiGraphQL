import graphene
from payments.schema import CreateCreditCard, MakePayment

class Mutation(graphene.ObjectType):

    create_creditcard = CreateCreditCard.Field()

    make_payment = MakePayment.Field()
