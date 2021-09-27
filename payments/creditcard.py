from payments.repo import CreditRepoInterface

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

    