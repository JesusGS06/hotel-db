from pydantic import BaseModel, Field, EmailStr

class CreateClient(BaseModel):
    first_name: str = Field(..., description="Client's first name")
    last_name: str = Field(..., description="Client's last name")
    email: EmailStr = Field(..., description="Client's email")
    phone: str = Field(..., description="Client's phone number")

class Client(CreateClient):
    client_id: int = Field(..., description="Client's unique ID") 