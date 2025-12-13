
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from .routers import (
    bias,
    privacy,
    data_ingestion,
    preprocessing,
    simulation,
    dashboard
)

app = FastAPI(title="V2V Bias Safety Lab API")


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register Routers
app.include_router(bias.router, prefix="/bias", tags=["Bias Detection"])
app.include_router(privacy.router, prefix="/privacy", tags=["Privacy Audit"])
app.include_router(data_ingestion.router, prefix="/data", tags=["Data Ingestion"])
app.include_router(preprocessing.router, prefix="/preprocess", tags=["Preprocessing"])
app.include_router(simulation.router, prefix="/sim", tags=["Simulation Engine"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard Service"])


@app.get("/")
def home():
    return {"message": "V2V Bias Safety Lab API is running 🚀"}
