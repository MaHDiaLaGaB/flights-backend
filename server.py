from fastapi import FastAPI
from api import health, users, booking
from config import Config
import uvicorn


app = FastAPI(docs_url="/")
app.include_router(health.route)
app.include_router(users.route)
app.include_router(booking.route)


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=Config.API_PORT)
