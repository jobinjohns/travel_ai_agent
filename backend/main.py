# main.py
# ---------------------------------------------------------
# The application entrypoint. Start the server with:
#   uvicorn main:app --reload --port 8000
# Then open http://localhost:8000/docs for the interactive
# Swagger API docs, generated automatically from schemas.py.
# ---------------------------------------------------------
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routes import auth, users, plan

# Creates every table defined in models.py, if it doesn't exist yet.
# (For a bigger production app you'd use Alembic migrations instead —
# create_all() is simpler and perfectly fine for a portfolio project.)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Travel Operations Agent")

# CORS = Cross-Origin Resource Sharing. Without this, a browser
# blocks the frontend (a different "origin," e.g. a file:// page or
# localhost:5500) from calling this API on localhost:8000.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # in production, list your real frontend URL instead of "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

# Plug in our route files
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(plan.router)


@app.get("/")
def root():
    # A simple health-check route — visiting http://localhost:8000/
    # should show this JSON if the server is running correctly
    return {"status": "AI Travel Operations Agent API is running"}
