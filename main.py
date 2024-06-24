from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from predictor import get_predictions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def get():
    with open("static/index.html") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)


@app.post("/predict")
async def predict(request: Request):
    data = await request.json()
    text = data.get("text", "")
    text += " <mask>"
    suggestions = get_predictions(text)
    return {"suggestions": suggestions}
