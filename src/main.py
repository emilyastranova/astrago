from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import database

app = FastAPI(
    title="astrago",
    description="A simple and fast shortlink service.",
    version="0.1.0",
)

templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def startup_event():
    """On startup, create the database table if it doesn't exist."""
    database.create_table()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Root endpoint that displays the link management UI.
    """
    links = database.get_all_links()
    return templates.TemplateResponse("manage.html", {"request": request, "links": links})


@app.post("/create-link")
async def create_link(name: str = Form(...), url: str = Form(...)):
    """
    Handles the form submission to create a new shortlink.
    """
    if not url.startswith("http://") and not url.startswith("https://"):
        url = f"https://{url}"
    database.add_link(name, url)
    return RedirectResponse(url="/", status_code=303)


@app.post("/delete-link")
async def delete_link_route(name: str = Form(...)):
    """
    Handles the form submission to delete a shortlink.
    """
    database.delete_link(name)
    return RedirectResponse(url="/", status_code=303)


@app.post("/rename-link")
async def rename_link_route(old_name: str = Form(...), new_name: str = Form(...)):
    """
    Handles the form submission to rename a shortlink.
    """
    database.rename_link(old_name, new_name)
    return RedirectResponse(url="/", status_code=303)


@app.post("/update-link")
async def update_link_route(name: str = Form(...), url: str = Form(...)):
    """
    Handles the form submission to update a shortlink's URL.
    """
    if not url.startswith("http://") and not url.startswith("https://"):
        url = f"https://{url}"
    database.update_link_url(name, url)
    return RedirectResponse(url="/", status_code=303)


@app.get("/{query:path}", response_class=HTMLResponse)
async def redirect_query(request: Request, query: str):
    """
    Redirects a shortlink query to its destination URL.

    If the shortlink (`query`) is found in the database, the user is
    redirected with a 307 Temporary Redirect.

    If the shortlink is not found, an HTML page is shown, asking the
    user if they want to create the link.
    """
    # Browsers will often request this, so we can safely ignore it.
    if query == "favicon.ico":
        return

    destination_url = database.get_link(query)
    if destination_url:
        return RedirectResponse(url=destination_url, status_code=307)
    else:
        return templates.TemplateResponse("not_found.html", {"request": request, "query": query})
