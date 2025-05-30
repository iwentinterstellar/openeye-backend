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
        # 🧠 Initialize conversation history for this WebSocket
        messages = [{"role": "system", "content": "You are a helpful assistant named OpenEye."}]

        while True:
            data = await websocket.receive_text()
            print("User said:", data)

            # Add user's new message
            messages.append({"role": "user", "content": data})
            print("Sending to OpenAI...")

            # Stream assistant response
            response = await openai.ChatCompletion.acreate(
                model="gpt-4-turbo",
                messages=messages,
                stream=True
            )

            assistant_reply = ""
            async for chunk in response:
                content = chunk["choices"][0].get("delta", {}).get("content")
                if content:
                    assistant_reply += content
                    await websocket.send_text(content)

            await websocket.send_text("[END]")

            # Save assistant's full reply to conversation history
            messages.append({"role": "assistant", "content": assistant_reply})

    except Exception as e:
        print("WebSocket error:", e)
        await websocket.close()
