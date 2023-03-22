from bme.saved_types.sequence import Sequence

from bme.config import default_bookmarks_location, default_sequences_location
from fastapi import FastAPI
from fastapi import Request

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to BME Daemon API"}


@app.get("/bookmarks")
async def fetch_bookmarks():
    from bme.saved_types.bookmark import Bookmark
    return Bookmark.load_all(default_bookmarks_location, force_json=True)


@app.post("/bookmark")
async def update_bookmark(info: Request):
    from bme.saved_types.bookmark import Bookmark
    req_info = await info.json()
    Bookmark.overwrite(req_info, default_bookmarks_location, force_json=True)


@app.get("/sequences")
async def fetch_sequences():
    from bme.saved_types.bookmark import Bookmark
    return Sequence.load_all(default_sequences_location, force_json=True)


@app.post("/sequence/{name}")
async def update_seq(info: Request, name: str):
    req_info = await info.json()
    from bme.saved_types.sequence import Sequence
    Sequence.overwrite(req_info, default_sequences_location, force_json=True)
