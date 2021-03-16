from fastapi import FastAPI, Depends, HTTPException, Request, Response, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder

from ml_models import *
from pythainlp import word_vector,word_tokenize
# from pythainlp.ulmfit import process_thai
from datetime import datetime

app=FastAPI(title="Activity Time Collector")

templates = Jinja2Templates(directory='templates')

model_loader=ModelLoader()

@app.get("/",response_class=HTMLResponse)
async def main(request: Request):
    # return "This is the first page"
    meta_dict=model_loader.get_meta()
    return templates.TemplateResponse('mainpage.html',{"request": request,"meta_dict":meta_dict})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            time1=datetime.now()
            answer = model_loader.predict(data)
            time2=datetime.now()
            time_diff=time2-time1
            print(time_diff.total_seconds())
            # await websocket.send_text(f"Message text was: {answer}")
            await websocket.send_json({'answer':answer,"time_elapsed":time_diff.total_seconds()})
    except WebSocketDisconnect:
        print("Web Socket Disconnect")