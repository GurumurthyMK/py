from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

posts: list[dict] = [
    {
        "id": 1,
        "title": "Getting Started with FastAPI",
        "content": "A quick introduction to building APIs with FastAPI.",
    },
    {
        "id": 2,
        "title": "Python Type Hints",
        "content": "Why type hints make Python code easier to maintain.",
    },
    {
        "id": 3,
        "title": "Working with Databases",
        "content": "Notes on connecting an API to a database.",
    },
    {
        "id": 4,
        "title": "Testing Your Endpoints",
        "content": "A few practical ways to test API routes.",
    },
    {
        "id": 5,
        "title": "Deploying a FastAPI App",
        "content": "Steps to prepare a FastAPI project for deployment.",
    },
]


@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):
    return templates.TemplateResponse(
        request, "home.html", {"posts": posts, "title": "Home"}
    )


@app.get("/api/posts")
def get_posts():
    return posts
