from fastapi import FastAPI
import uvicorn
app = FastAPI()

@app.get("/")
async def read_msg():
    return ({"message":"new message"})

@app.get('/greet/{name}')
async def greet_name(name:str)->dict:
    return {"message": f"Hello {name}"}