from pydantic import BaseModel, Field
from datetime import date
from typing import List

class CreateReservation(BaseModel):
    client_id: int = Field(..., description="Client's ID")
    room_id: int = Field(..., description="Room's ID")
    start_date: date = Field(..., description="Reservation start date")
    end_date: date = Field(..., description="Reservation end date")

class Reservation(CreateReservation):
    reservation_id: int = Field(..., description="Reservation's unique ID") 