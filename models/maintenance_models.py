from pydantic import BaseModel, Field
from datetime import date as date_type

class CreateMaintenance(BaseModel):
    room_id: int = Field(..., description="Room's ID")
    maintenance_date: date_type = Field(..., description="Maintenance date")
    description: str = Field(..., description="Maintenance description")

class Maintenance(CreateMaintenance):
    maintenance_id: int = Field(..., description="Maintenance's unique ID") 