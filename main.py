from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


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


@app.get("/posts", response_class=HTMLResponse, include_in_schema=False)
def home():
    return f"<h1>{posts[0]['title']}</h1>"


@app.get("/api/posts")
def get_posts():
    return posts
