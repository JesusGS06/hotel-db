from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import (
    client_router,
    room_router,
    reservation_router,
    service_router,
    payment_router,
    maintenance_router,
    reports_router
)

app = FastAPI(title="Hotel Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  
    allow_credentials=True,
    allow_methods=["GET", "POST"], 
    allow_headers=["*"],
)

app.include_router(client_router)
app.include_router(room_router)
app.include_router(reservation_router)
app.include_router(service_router)
app.include_router(payment_router)
app.include_router(maintenance_router)
app.include_router(reports_router)

@app.get("/")
def read_root():
    return {"message": "API is running"}