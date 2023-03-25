from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from src.routes import auth, channels

# Initalise app
app = FastAPI(
    title='Spotify GPT App',
    description="""
    This is a FastAPI microservice for a Spotify + Open AI integrated service
    """,
    version='0.1.0'
)

# Add middleware
app.add_middleware(SessionMiddleware, secret_key="secret_key_placeholder")


# Routers
app.include_router(auth.router)
app.include_router(channels.router)