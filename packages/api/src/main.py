from fastapi import FastAPI
from src.routes import playlists, auth, tests
from fastapi.middleware.cors import CORSMiddleware

# Initalise app
app = FastAPI(
    title='Spotify GPT App',
    description="""
    This is a FastAPI microservice for a Spotify + Open AI integrated service
    """,
    version='0.1.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
# app.include_router(auth.router)
# app.include_router(playlists.router)
app.include_router(tests.router)