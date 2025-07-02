from fastapi import FastAPI, Body
from dotenv import load_dotenv
from openai import OpenAI
import os

app = FastAPI()

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

@app.post("/")
def analysis(text: str = Body(...)) -> str:
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
        return response.output_text
    except Exception as e:
        return f"Error: {str(e)}"

@app.get("/")
async def root():
    return "App is running on port 8000"
