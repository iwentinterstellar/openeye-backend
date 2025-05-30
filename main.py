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

    # 🧠 Persistent memory for chat context
    messages = [
        {"role": "system", "content": "You are OpenEye, a helpful and conversational assistant. Respond with clarity and personality."}
    ]

    try:
        while True:
            data = await websocket.receive_text()
            print("User said:", data)

            # Add user's message to memory
            messages.append({"role": "user", "content": data})

            # Stream OpenAI response
            response = await openai.ChatCompletion.acreate(
                model="gpt-4-turbo",
                messages=messages,
                stream=True
            )

            full_reply = ""

            async for chunk in response:
                content = chunk["choices"][0].get("delta", {}).get("content")
                if content:
                    full_reply += content
                    await websocket.send_text(content)

            # Add assistant's response to memory
            messages.append({"role": "assistant", "content": full_reply})
            await websocket.send_text("[END]")

    except Exception as e:
        print("WebSocket error:", e)
        await websocket.close()
