from pydantic import BaseModel, Field
from decimal import Decimal

class CreateService(BaseModel):
    name: str = Field(..., description="Service name")
    description: str = Field(..., description="Service description")
    cost: Decimal = Field(..., description="Service cost")

class Service(CreateService):
    service_id: int = Field(..., description="Service's unique ID")

class CreateReservationService(BaseModel):
    reservation_id: int = Field(..., description="Reservation's ID")
    service_id: int = Field(..., description="Service's ID")
    quantity: int = Field(..., description="Quantity of services")

class ReservationService(CreateReservationService):
    reservation_service_id: int = Field(..., description="Reservation service's unique ID") 