from fastapi import FastAPI
from pydantic import BaseModel
import cohere
from dotenv import load_dotenv
import os

load_dotenv()

class chatRequest(BaseModel):
    prompt: str

class chatResponse(BaseModel):
    response: str

app = FastAPI()
co = cohere.ClientV2(api_key=os.getenv("API_KEY"))

@app.get("/")
def health():
    return {"status": "Ok! This is working woohoo!"}

@app.post("/chat", response_model=chatResponse)
def chat(request: chatRequest):
    
    user_prompt = request.prompt
    
    response = co.chat(
        model="command-a-03-2025",
        messages=[{"role": "user", "content": user_prompt}],
    )

    final_response = response.message.content[0].text

    return chatResponse(response=f"Cohere said this: {final_response}")