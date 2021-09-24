from fastapi.testclient import TestClient
import graphene

from payments.creditcard import CreditCard
from payments.app import app, QueryPerson, MutationCreditCard


CLIENT = TestClient(app)



def test_creditcard_deduct_value():
    creditcard = CreditCard(budget=200, card_id='a')
    creditcard.deduct(150)
    assert creditcard.budget == 50

def test_api_endpoint_is_available():
    response = CLIENT.post('/payments/a', json={'amount_to_deduct': 50})
    assert response.json() == {'budget': 450}

def test_graph_endpoint():
    query= """
    {
        hello(name: "FastApi")
    }
    """
    result = CLIENT.post("/graph", json={"query": query})
    assert "Hello" in result.json().get("data").get('hello')


def test_query_person_data():
    schema = graphene.Schema(query=QueryPerson)
    result = schema.execute("""
        query CreditCardQuery {
            me(name: "Stef") { firstName lastName}
            myBestFriend { firstName lastName }
            allCreditcards { budget }
        }
    """)
    # With default resolvers we can resolve attributes from an object..
    assert result.data["me"] == {"firstName": "Stef", "lastName": "Skywalker"}

    # With default resolvers, we can also resolve keys from a dictionary..
    assert result.data["myBestFriend"] == {"firstName": "R2", "lastName": "D2"}

    assert result.data["allCreditcards"] == [{"budget": 500}, {"budget": 900}, {"budget": 200}]

# def test_create_creditcard():
#     schema = graphene.Schema(query=QueryPerson, mutation=MutationCreditCard)

#     result = schema.execute('''
#         mutation CreateCreditCard {
#             createCreditcard(initial_budget: 0, card_id: "z") { 
#                 creditcard { 
#                     budget 
#                 } 
#             }
#         }
#     ''')
#     assert result.data["createCreditCard"] == {"budget": 0, "card_id": "z"}

def test_mutation():
    class Person(graphene.ObjectType):
        name = graphene.String()
        age = graphene.Int()


    # We must define a query for our schema
    class Query(graphene.ObjectType):
        person = graphene.Field(Person)

    class CreatePerson(graphene.Mutation):
        class Arguments:
            name = graphene.String()

        ok = graphene.Boolean()
        person = graphene.Field(Person)

        def mutate(root, info, name):
            person = Person(name=name)
            ok = True
            return CreatePerson(person=person, ok=ok)

    class MyMutations(graphene.ObjectType):
        create_person = CreatePerson.Field()
    schema = graphene.Schema(query=Query, mutation=MyMutations) 
    result = schema.execute("""
    mutation myFirstMutation {
        createPerson(name:"Peter") {
            person {
                name
            }
            ok
        }
    }""")
    assert result.data == {
    "createPerson": {
        "person" : {
            "name": "Peter"
        },
        "ok": True
    }
}

def test_create_creditcard():
    query = '''
        mutation CreateCreditCard {
            createCreditcard(initialBudget: 0, cardId: "z") { 
                creditcard { 
                    budget 
                    cardId
                } 
            }
        }
    '''
    result = CLIENT.post("/creditcard", json={"query": query}).json()
    assert result["data"]["createCreditcard"]['creditcard'] == {"budget": 0, "cardId": "z"}