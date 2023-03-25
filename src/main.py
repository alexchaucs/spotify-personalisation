from fastapi import FastAPI
from src.routes import auth, channels

# Initalise app
app = FastAPI(
    title='Spotify GPT App',
    description="""
    This is a FastAPI microservice for a Spotify + Open AI integrated service
    """,
    version='0.1.0'
)

# Routers
app.include_router(auth.router)
app.include_router(channels.router)