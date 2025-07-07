import logging
from graphene import Schema
from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette_graphene3 import GraphQLApp, make_playground_handler
from back_api.gql.queries import Query
from back_api.db.database import prepare_database
from back_api.gql.mutations import Mutation
from fastapi.middleware.cors import CORSMiddleware
import logging
from back_api.utils.filter_logs import HealthCheckFilter

# Disable logging for the health check endpoint
logging.getLogger("uvicorn.access").addFilter(HealthCheckFilter())

schema = Schema(query=Query, mutation=Mutation)

@asynccontextmanager
async def lifespan(app: FastAPI):
    prepare_database()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

app.mount("/graphql", GraphQLApp(
    schema=schema,
    on_get=make_playground_handler()
))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
