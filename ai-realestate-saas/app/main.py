from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine, Base
from app.api.routers import auth, leads, conversations, appointments, followups

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Real Estate SaaS Platform",
    description="Multi-Tenant AI Real Estate CRM Backend",
    version="2.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "AI Real Estate SaaS Engine"}

app.include_router(auth.router)
app.include_router(leads.router)
app.include_router(conversations.router)
app.include_router(appointments.router)
app.include_router(followups.router)