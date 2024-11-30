from fastapi import FastAPI
import uvicorn
app = FastAPI()

@app.get("/")
async def read_msg():
    return ({"message":"new message"})