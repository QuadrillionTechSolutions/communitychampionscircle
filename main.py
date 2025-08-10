import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.templating import Jinja2Templates

from routers import public, auth_routes, profiles, chat, projects, events, updates, admin, calls
from payments import router as payments_router

app = FastAPI(title="Community Champions Circle")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.state.templates = templates

app.include_router(public.router)
app.include_router(auth_routes.router)
app.include_router(profiles.router)
app.include_router(chat.router)
app.include_router(projects.router)
app.include_router(events.router)
app.include_router(updates.router)
app.include_router(admin.router)
app.include_router(calls.router)
app.include_router(payments_router)

@app.get("/health")
def health():
    return {"ok": True}
