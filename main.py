from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from predictor import get_top_predictions

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware to allow all origins, methods, and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")


# Define the root endpoint to serve the HTML file
@app.get("/")
async def get_root():
    with open("static/index.html") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)


# Define the prediction endpoint
@app.post("/predict")
async def predict(request: Request):
    data = await request.json()
    text = data.get("text", "")
    text += " <mask>"
    suggestions = get_top_predictions(text)
    return {"suggestions": suggestions}
