from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

app = FastAPI()

templates = Jinja2Templates(directory="templates")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def analysis(request: Request, text: str = Form(...)):
    try:
        response = client.responses.create(
            model="gpt-4.1",
            input=f"Please analyze the following text according to these criteria:\n\n"
                  f"1. Grammar Accuracy\n"
                  f"2. Clarity and Readability\n"
                  f"3. Structure and Logic\n"
                  f"4. Lexical Diversity\n"
                  f"5. Style and Tone\n"
                  f"6. Content Relevance\n"
                  f"7. Originality\n"
                  f"8. Length Appropriateness\n"
                  f"9. Coherence and Cohesion\n"
                  f"10. Keyword Usage\n\n"
                  f"Give your feedback as plain text, listing each criterion and a short comment on it. Ensure each new criterion starts on a new line.\n\n"
                  f"Text:\n"
                  f"{text}"
        )
        feedback = response.output_text
    except Exception as e:
        feedback = f"Error: {str(e)}"
    return templates.TemplateResponse("result.html", {"request": request, "feedback": feedback, "original_text": text})

@app.get("/health")
async def health_check():
    return {"status": "App is running"}

