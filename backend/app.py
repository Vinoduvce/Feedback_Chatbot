from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from chat import Chatbot

app = FastAPI()
chatbot_instance = Chatbot() 

# app.mount("/static", StaticFiles(directory="static"), name="static")

# @app.get("/")
# async def get():
#     return FileResponse("static/chat.html")

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            bot_response = chatbot_instance.handle_input(message)
            await websocket.send_text(bot_response)
    except WebSocketDisconnect:
        print("Websocket disconnected")

