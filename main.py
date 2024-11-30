from fastapi import FastAPI
import uvicorn
app = FastAPI()

@app.get("/")
async def read_msg():
    return ({"message":"new message"})

@app.get('/greet/{name}')
async def greet_name(name:str)->dict:
    return {"message": f"Hello {name}"}

#Query parameter-->
@app.get('/greet')
async def greet_name(name:str)->dict:
    return {"message": f"Hello {name}"}

#Query and Path parameter
@app.get('/greet/{name}')
async def greet_name(name:str, age:int)->dict:
    return {"message": f"Hello {name}", "age":age}