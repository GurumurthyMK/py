from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

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


@app.get("/", name="home")
@app.get("/posts", name="posts")
def home(request: Request):
    return templates.TemplateResponse(
        request, "home.html", {"posts": posts, "title": "Home"}
    )


# API routes
@app.get("/api/posts/{post_id}", include_in_schema=False)
def get_posts(post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.exception_handler(StarletteHTTPException)
def general_http_exception(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "There is some error, please try again"
    )
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"Detail": message},
        )

    return templates.TemplateResponse(
        request,
        "errors.html",
        {
            "Status code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )

    return templates.TemplateResponse(
        request,
        "errors.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invlid request, please try again later",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )
