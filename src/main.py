from fastapi import FastAPI
from src.routes import auth, channels

# Initalise app
app = FastAPI(
    title='Boiler plate api',
    description="""
    This is a FastAPI boilet plate code
    """,
    version='0.1.0'
)

# Routers
app.include_router(auth.router)
app.include_router(channels.router)