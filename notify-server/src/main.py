import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from fastapi import FastAPI

from send_notify.router import router as send_notify_router
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(send_notify_router)
