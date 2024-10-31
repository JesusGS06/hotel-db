from pydantic import BaseModel, Field
from enum import Enum
from decimal import Decimal

class RoomStatus(str, Enum):
    AVAILABLE = "Available"
    OCCUPIED = "Occupied"
    MAINTENANCE = "Maintenance"

class CreateRoom(BaseModel):
    room_number: str = Field(..., description="Room number")
    type: str = Field(..., description="Room type")
    price: Decimal = Field(..., description="Room price per night")
    status: RoomStatus = Field(..., description="Current room status")

class Room(CreateRoom):
    room_id: int = Field(..., description="Room's unique ID") 