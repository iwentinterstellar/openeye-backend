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
    messages = [
        {"role": "system", "content": "You are OpenEye, a helpful and conversational assistant. Respond with clarity and personality."}
    ]
    try:
        # 🧠 Initialize conversation history for this WebSocket
        messages = [{"role": "system", "content": "You are a helpful assistant named OpenEye."}]

        while True:
            data = await websocket.receive_text()
            print("User said:", data)

<<<<<<< HEAD
            # Add user's new message
            messages.append({"role": "user", "content": data})
            print("Sending to OpenAI...")
=======
            messages.append({"role": "user", "content": data})
>>>>>>> 1e75caa (Enable memory for chat history)

            # Stream assistant response
            response = await openai.ChatCompletion.acreate(
                model="gpt-4-turbo",
                messages=messages,
                stream=True
            )

<<<<<<< HEAD
            assistant_reply = ""
=======
            full_reply = ""
>>>>>>> 1e75caa (Enable memory for chat history)
            async for chunk in response:
                content = chunk["choices"][0].get("delta", {}).get("content")
                if content:
                    assistant_reply += content
                    await websocket.send_text(content)
                    full_reply += content

            messages.append({"role": "assistant", "content": full_reply})
            await websocket.send_text("[END]")

            # Save assistant's full reply to conversation history
            messages.append({"role": "assistant", "content": assistant_reply})

    except Exception as e:
        print("WebSocket error:", e)
        await websocket.close()
<<<<<<< HEAD
=======

>>>>>>> 1e75caa (Enable memory for chat history)
