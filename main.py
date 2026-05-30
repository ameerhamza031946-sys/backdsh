from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.mongodb import connect_to_mongo, close_mongo_connection
from routes import auth, users, posts

app = FastAPI(title="Production Ready FastAPI Backend")

# CORS setup
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:8000"
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection events
@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

# Include Routers
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1", tags=["Users"])
app.include_router(posts.router, prefix="/api/v1/posts", tags=["Posts"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the FastAPI Backend!"}
