from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os

app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY")

class StoryRequest(BaseModel):
    name: str
    topic: str

@app.post("/generate-story")
async def generate_story(req: StoryRequest):
    prompt = f"Napisz bajkę dla dziecka o imieniu {req.name} na temat: {req.topic}. Zakończ bajkę podziękowaniem i życzeniami spokojnej nocy."

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            temperature=0.7,
        )
        story = response.choices[0].text.strip()
        return {"story": story}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
