from fastapi import FastAPI, HTTPException, Request, status
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


# HTML routes
@app.get("/posts/{post_id}")
def post_page(post_id: int, request: Request):
    for post in posts:
        if post.get("id") == post_id:
            title = post["title"][:50]
            return templates.TemplateResponse(
                request, "post.html", {"post": post, "title": title}
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):
    return templates.TemplateResponse(
        request, "home.html", {"posts": posts, "title": "Home"}
    )


# API routes
@app.get("/api/posts/{post_id}")
def get_posts(post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
