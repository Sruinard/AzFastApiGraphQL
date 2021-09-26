from pydantic import BaseModel
import graphene
from typing import List


class CreditCardObject(graphene.ObjectType):
    budget = graphene.Int()
    card_id = graphene.ID()

    def add_payment(self, amount):
        self.budget = self.budget - amount


class CreateCreditCard(graphene.Mutation):
    # specify inputs
    class Arguments:
        initial_budget = graphene.Int()
        card_id = graphene.String()

    # specify outputs
    creditcard = graphene.Field(CreditCardObject)

    def mutate(root, info, initial_budget, card_id):
        repo = CreditCardRepoImpl()
        creditcard = CreditCardObject(budget=initial_budget, card_id=card_id)
        repo.add(
            card=creditcard
        ) 
        return CreateCreditCard(creditcard=creditcard)

class MakePayment(graphene.Mutation):
    # specify inputs
    class Arguments:
        amount = graphene.Int()
        receiver_id = graphene.String()
        sender_id = graphene.String()

    # specify outputs
    sender_card = graphene.Field(CreditCardObject)
    receiver_card = graphene.Field(CreditCardObject)


    def mutate(root, info, receiver_id, sender_id, amount):
        repo = CreditCardRepoImpl()  
        payment_usecase = PaymentsSystem(repo=repo)
        payment = Payment(receiver_id, sender_id, amount)
        payment_usecase.make_payment(payment)
        sender_card = repo.get(id=sender_id)
        receiver_card = repo.get(id=receiver_id)
        return MakePayment(sender_card=sender_card, receiver_card=receiver_card)

# class CreditCardRepo:

#     def __init__(self) -> None:
#         self.items = [CreditCardObject(card_id=card_id, budget=budget) for card_id, budget in list(zip(["a", "b", "c"], [500, 900, 200]))]

#     def get_item_by_card_id(self, card_id):
#         creditcard = [item for item in self.items if item.card_id == card_id][0]
#         return creditcard
    
#     def get_all_cards(self):
#         return self.items         

#     def create(self, initial_budget):
#         new_creditcard = CreditCardObject(budget=initial_budget, card_id="g")
#         self.items.append(new_creditcard) 
#         return new_creditcard 





        
ITEMS = [CreditCardObject(card_id=card_id, budget=budget) for card_id, budget in list(zip(["a", "b", "c"], [500, 900, 200]))]

class CreditRepoInterface:

    def get(self, id):
        raise NotImplementedError 

    def get_cards(self, ids: List[str]):
        raise NotImplementedError

    def get_all_cards(self):
        raise NotImplementedError

    def add(self, card: CreditCardObject):
        raise NotImplementedError

    def update_all(self, items: List[CreditCardObject]):
        raise NotImplementedError

class CreditCardRepoImpl(CreditRepoInterface):

    def get(self, id):
        return [item for item in ITEMS if item.card_id == id][0]

    def get_cards(self, ids):
        cards = [item for item in ITEMS if item.card_id in ids]
        return cards

    def get_all_cards(self):
        return ITEMS

    def add(self, card: CreditCardObject):
        ITEMS.append(card)
        return card

    def update_all(self, items):
        for item_to_update in items:
            for index, item in enumerate(ITEMS):
                if item_to_update.card_id == item.card_id:
                    ITEMS[index] = item_to_update
        return items

class Payment:

    def __init__(self, card_receiver_id, card_sender_id, amount):
        self.card_receiver_id = card_receiver_id
        self.card_sender_id = card_sender_id
        self.amount = amount

class PaymentsSystem:

    def __init__(self, repo: CreditRepoInterface):
        self.repo = repo
        
    def make_payment(self, payment: Payment):
        receiver = self.repo.get(payment.card_receiver_id)
        receiver.add_payment(amount=-payment.amount)
        sender = self.repo.get(payment.card_sender_id)
        sender.add_payment(amount=payment.amount)
        self.repo.update_all([sender, receiver])
        return payment

    