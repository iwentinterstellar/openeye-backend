from fastapi import FastAPI, WebSocket
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print("User said:", data)

            messages = [{"role": "user", "content": data}]
            print("Sending request to OpenAI...")

            response = await openai.ChatCompletion.acreate(
                model="gpt-4-turbo",
                messages=messages,
                stream=True
            )

            async for chunk in response:
                content = chunk["choices"][0].get("delta", {}).get("content")
                if content:
                    await websocket.send_text(content)

            await websocket.send_text("[END]")

    except Exception as e:
        print("WebSocket error:", e)
        await websocket.close()
