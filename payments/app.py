from fastapi import FastAPI
from fastapi import FastAPI
import graphene
from starlette.graphql import GraphQLApp
from payments.schema import Query, Mutation

app = FastAPI()
app.add_route("/creditcard", GraphQLApp(schema=graphene.Schema(query=Query, mutation=Mutation)))

@app.get("/")
def homepage():
    return "Fast API + GraphQL"
